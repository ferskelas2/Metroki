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

    def setup_play(self):
        self.state = 'GG'
        self.old_regions = None
        pass

    def find_sprite(self, path, game_frame=None, screen_region=None, use_global_location=True):
        locations = []

        frame = game_frame.grayscale_frame

        if screen_region is not None:
            frame = serpent.cv.extract_region_from_image(frame, screen_region)

        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        res = cv2.matchTemplate(frame, image, cv2.TM_CCOEFF_NORMED)
        threshold = .5
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

    def get_middle(self, region):
        x = (region[2] + region[0]) / 2
        y = (region[3] + region[1]) / 2
        return x, y

    def drag_mouse(self, points):
        for i, point in enumerate(points, start=1):
            self.input_controller.move(x=point[0], y=point[1])
            if i == 1:
                self.input_controller.click_down(MouseButton.LEFT)
            if i == len(points):
                self.input_controller.click_up(MouseButton.LEFT)
        pass

    def find_points(self, regions, old_regions=None):
        points = []
        if old_regions is None:
            old_regions = []
        for region in regions:
            point = self.get_middle(region)
            add = True
            for old in old_regions:
                if point_in_region(point, old):
                    add = False
                    break
            points.append(point)
            old_regions.append(region)
        return points, old_regions

    def point_in_region(self, point, region):
        x1, y1, x2, y2 = region
        x, y = point
        if x1 < x < x2 and y1 < y < y2:
            return True
        return False

    def handle_play(self, game_frame):
        if self.state == 'MM':
            self.state = 'LS'
            self.input_controller.click_screen_region(MouseButton.LEFT, "MM_Start")

        if self.state == 'LS':
            self.state = 'GG'
            time.sleep(4)
            self.input_controller.click_screen_region(MouseButton.LEFT, "LS_Start")

        if self.state == 'GG':
            game_region = self.game.screen_regions["Game"]
            squares = self.find_sprite(path=self.game.sprite_paths['Square'], game_frame=game_frame)
            circles = self.find_sprite(path=self.game.sprite_paths['Circle'], game_frame=game_frame)
            triangles = self.find_sprite(path=self.game.sprite_paths['Triangle'], game_frame=game_frame)

            regions = []

            if squares is not None:
                regions.append(squares)

            if circles is not None:
                regions.append(circles)

            if triangles is not None:
                regions.append(triangles)

            if self.old_regions is None:
                points, old = self.find_points(regions)
                self.old_regions = old
            else:
                points, old = self.find_points(regions, self.old_regions)
                self.old_regions = old


            self.drag_mouse(points)
#             if squares is not None and circles is not None:
#                 square = self.get_middle(squares[0])
#                 print(squares[0])
#                 print(square)
#
#                 circle = self.get_middle(circles[0])
#                 self.input_controller.drag(MouseButton.LEFT, square[0], square[1], circle[0], circle[1])



        pass
