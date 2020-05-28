import time
import cv2
import copy
import numpy as np
import skimage.io

import serpent.input_controller

from serpent.game_agent import GameAgent

from serpent.sprite import Sprite

from serpent.input_controller import KeyboardKey
from serpent.input_controller import MouseButton
from serpent.sprite_locator import SpriteLocator


class SerpentDragTestGameAgent(GameAgent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.frame_handlers["PLAY"] = self.handle_play

        self.frame_handler_setups["PLAY"] = self.setup_play

    # Setup für den Game Agent
    def setup_play(self):
        self.state = 'GG'
        self.old_regions = {'Squares': [], 'Circles': [], 'Triangles': []}
        pass

    # Sucht alle Vorkommnisse eines Bildes innerhalb eines anderen Bildes
    def find_sprites(self, path, game_frame=None, old_regions=[], debug=False, screen_region=None, use_global_location=True):
        locations = []

        frame = game_frame.grayscale_frame

        if screen_region is not None:
            frame = serpent.cv.extract_region_from_image(frame, screen_region)

        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        res = cv2.matchTemplate(frame, image, cv2.TM_CCOEFF_NORMED)
        threshold = .9
        loc = np.where(res >= threshold)
        if debug:
            print(old_regions)
        for pt in zip(*loc[::-1]):  # Switch collumns and rows
            valid = True
            location = [pt[0], pt[1], pt[0] + image.shape[0], pt[1] + image.shape[1]]
            point = self.get_middle(location)
            for old in old_regions:
                if self.point_in_region(point, old):
                    if debug:
                        print(old)
                    valid = False
                    pass
            if valid:
                if location is not None and screen_region is not None and use_global_location:
                    location = (
                        location[0] + screen_region[0],
                        location[1] + screen_region[1],
                        location[2] + screen_region[0],
                        location[3] + screen_region[1]
                    )
                old_regions.append(location)
                locations.append(location)
        old_regions = []
        if len(locations) != 0:
            return locations
        return None

    # Findet die Mitte einer Region
    def get_middle(self, region):
        x = (region[2] + region[0]) / 2
        y = (region[3] + region[1]) / 2
        return x, y

    # Zieht die Maus über einen array von Punkten
    def drag_mouse(self, points):
        for i, point in enumerate(points, start=1):
            self.input_controller.move(x=point[0], y=point[1])
            if i == 1:
                self.input_controller.click_down(MouseButton.LEFT)
            if i == len(points):
                self.input_controller.click_up(MouseButton.LEFT)
        pass

    # Sucht alle gültigen Punkte in einem array von Regionen
    def find_points(self, forms, old_regions=None):
        points = []
        if old_regions is None:
            old_regions = {}
        for form_type, form in forms.items():
            #Alle Regionen einer Form auf gültigen Punkt Untersuchen
            for region in form['regions']:
                point = self.get_middle(region)
                valid = True
                # Überprüfen ob der Punkt nicht schon angewählt wurde
                if form_type in old_regions:
                    for old in old_regions[form_type]:
                        if self.point_in_region(point, old):
                            valid = False
                            break
                # Punkt hinzufügen, wenn er gültig ist
                if valid:
                    points.append(point)
                    if form_type not in old_regions:
                        old_regions[form_type] = []
                    old_regions[form_type].append(region)
            # Wenn die Region wiederholt als Punkt ausgewählt werden soll, aus dem old_regions dictionary entfernen
            if form['parameters']['repeat']:
                old_regions[form_type] = []
        return points, old_regions

    # Überprüft ob ein Punkt sich in einer Region befindet
    # point = [x, y]
    # region = [x1, y1, x2, y2]
    def point_in_region(self, point, region):
        x1, y1, x2, y2 = region
        x, y = point
        if x1 < x < x2 and y1 < y < y2:
            return True
        return False

    # Bearbeiten, der einzelnen Game Frames
    def handle_play(self, game_frame):
        if self.state == 'MM':
            self.state = 'LS'
            self.input_controller.click_screen_region(MouseButton.LEFT, "MM_Start")

        if self.state == 'LS':
            self.state = 'GG'
            time.sleep(4)
            self.input_controller.click_screen_region(MouseButton.LEFT, "LS_Start")

        if self.state == 'GG':
            # Frame auf die einzelnen Sprites scannen
            old_copy = copy.deepcopy(self.old_regions)
            squares = self.find_sprites(path=self.game.sprite_paths['Square'], game_frame=game_frame, old_regions=old_copy['Squares'], debug=True)
            circles = self.find_sprites(path=self.game.sprite_paths['Circle'], game_frame=game_frame, old_regions=old_copy['Circles'])
            triangles = self.find_sprites(path=self.game.sprite_paths['Triangle'], game_frame=game_frame, old_regions=old_copy['Triangles'])
            old_copy = copy.deepcopy(self.old_regions)
            forms= {}

            # Die Sprites als Haltestation (stops) dictionary speichern
            if squares is not None:
                forms['Squares'] = {
                    'regions': squares,
                    'parameters': {
                        'repeat': True
                    }
                }
            if circles is not None:
                forms['Circles'] = {
                    'regions': circles,
                    'parameters': {
                        'repeat': False
                    }
                }
            if triangles is not None:
                forms['Triangles'] = {
                    'regions': triangles,
                    'parameters': {
                        'repeat': False
                    }
                }

            print(forms)

            # Alle gültigen Punkte aus der regions dictionary holen
            points, old = self.find_points(forms, old_copy)

            # Nur dann Punkte verbinden, wenn es mindestens 2 gibt
            if len(points) >= 2:
                self.old_regions = old
                self.drag_mouse(points)

            print(self.old_regions)

            #time.sleep(5)
        pass
