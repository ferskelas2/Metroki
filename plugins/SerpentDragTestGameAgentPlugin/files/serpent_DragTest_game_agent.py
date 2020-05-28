import time
import cv2
import os
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
        self.old_regions = None
        pass

    # Sucht alle Vorkommnisse eines Bildes innerhalb eines anderen Bildes
    def find_sprites(self, path, game_frame=None, screen_region=None, use_global_location=True):
        locations = []

        frame = game_frame.grayscale_frame

        if screen_region is not None:
            frame = serpent.cv.extract_region_from_image(frame, screen_region)

        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        res = cv2.matchTemplate(frame, image, cv2.TM_CCOEFF_NORMED)
        threshold = .9
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):  # Switch collumns and rows
            location = [pt[0], pt[1], pt[0] + image.shape[0], pt[1] + image.shape[1]]
            if location is not None and screen_region is not None and use_global_location:
                location = (
                    location[0] + screen_region[0],
                    location[1] + screen_region[1],
                    location[2] + screen_region[0],
                    location[3] + screen_region[1]
                )
            locations.append(location)
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
    def find_points(self, regions, old_regions=None):
        points = []
        if old_regions is None:
            old_regions = {}
        for reg_type, region in regions.items():
            for area in region['areas']:
                point = self.get_middle(area)
                add = True
                if reg_type in old_regions:
                    for old in old_regions[reg_type]:
                        if self.point_in_region(point, old):
                            add = False
                            break
                if add:
                    points.append(point)
                    if reg_type not in old_regions:
                        old_regions[reg_type] = []
                    old_regions[reg_type].append(area)
            if region['parameters']['repeat']:
                old_regions.pop(reg_type)
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
            #game_region = self.game.screen_regions["Game"]
            squares = self.find_sprites(path=self.game.sprite_paths['Square'], game_frame=game_frame)
            circles = self.find_sprites(path=self.game.sprite_paths['Circle'], game_frame=game_frame)
            triangles = self.find_sprites(path=self.game.sprite_paths['Triangle'], game_frame=game_frame)

            regions = {}

            if squares is not None:
                regions['Squares'] = {
                    'areas': squares,
                    'parameters': {
                        'repeat': True
                    }
                }
            if circles is not None:
                regions['Circles'] = {
                    'areas': circles,
                    'parameters': {
                        'repeat': False
                    }
                }
            if triangles is not None:
                regions['Triangles'] = {
                    'areas': triangles,
                    'parameters': {
                        'repeat': False
                    }
                }
            if self.old_regions is None:
                points, old = self.find_points(regions)
            else:
                points, old = self.find_points(regions, self.old_regions.copy())


            if len(points) >= 2:
                self.old_regions = old
                self.drag_mouse(points)

            #print(points)
            #print(regions)
            #print(self.old_regions)
        pass
