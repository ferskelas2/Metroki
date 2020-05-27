import time
import numpy as np
import skimage.io
import imageio
import cv2

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
        self.state = 'MM'
        pass

    def find_sprite(self, sprite, game_frame=None, screen_region=None, mode="SIGNATURE_COLORS", use_global_location=True):
        #constellation_of_pixel_images = sprite.generate_constellation_of_pixels_images()
        location = None

        sp_image = sprite.image_data,


#         row, col ,ch = sp_image.shape
#
#         if ch != 3:
#             rgb = np.zeros((row, col, 3), dtype='float32')
#             r, g, b, a = sp_image[:,:,0], sp_image[:,:,1], sp_image[:,:,2], sp_image[:,:,3]
#             a = np.asarray(a, dtype='float32') / 255.0
#
#             rgb[:,:,0] = r * a + (1.0 - a) * 255
#             rgb[:,:,1] = g * a + (1.0 - a) * 255
#             rgb[:,:,2] = b * a + (1.0 - a) * 255
#
#             sp_image = np.asarray(rgb, dtype='uint8')

        sp_image = cv2.cvtColor(sp_image, cv2.COLOR_BGR2GRAY)


        res = cv2.matchTemplate(game_frame.grayscale_frame, sp_image, cv2.TM_CCOEFF_NORMED)
        threshold = .8
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            location = (
                pt[0],
                pt[1],
                pt[0] + sprite.image_data.shape[0],
                pt[1] + sprite.image_data.shape[1],
            )
            return location
        return location
#         frame = game_frame.frame
#
#         if screen_region is not None:
#             frame = serpent.cv.extract_region_from_image(frame, screen_region)
#
#         maximum_y = frame.shape[0] - sprite.image_data.shape[0]
#         maximum_x = frame.shape[1] - sprite.image_data.shape[1]
#
#         for x in range(0, maximum_x):
#             for y in range(0, maximum_y):
#                 region = (x, y, x+sprite.image_data.shape[0], y+sprite.image_data.shape[1])
#                 query_sprite = Sprite("QUERY", image_data=serpent.cv.extract_region_from_image(frame, region)[..., np.newaxis])
#                 name = self.sprite_identifier.identify(query_sprite, mode=mode)
#                 if name == sprite.name:
#                     location = region
#
#                     if location is not None and screen_region is not None and use_global_location:
#                         location = (
#                             location[0] + screen_region[0],
#                             location[1] + screen_region[1],
#                             location[2] + screen_region[0],
#                             location[3] + screen_region[1]
#                         )
#
#                     return location
#         return location
        pass

    def handle_play(self, game_frame):
        if self.state == 'MM':
            self.state = 'LS'
            self.input_controller.click_screen_region(MouseButton.LEFT, "MM_Start")

        if self.state == 'LS':
            self.state = 'GG'
            time.sleep(4)
            self.input_controller.click_screen_region(MouseButton.LEFT, "LS_Start")

        if self.state == 'GG':
            #image_data = skimage.io.imread("C:\\Users\\anton\\PycharmProjects\\Metroki\\plugins\\SerpentminimetroGamePlugin\\files\\data\\sprites\\sprite_square_0.png")[..., np.newaxis]

            #sprite = Sprite("MY SPRITE", image_data=image_data)

            #query_sprite = Sprite("QUERY", image_data=image_data)
            #sprite_name = self.sprite_identifier.identify(query_sprite, mode="SIGNATURE_COLORS")
            #print(sprite_name)

            #sprite_circle = self.game.sprites['SPRITE_CIRCLE']
            sprite_square = self.game.sprites['SPRITE_SQUARE']
            #sprite_triangle = self.game.sprites['SPRITE_TRIANGLE']

            #sprite_locator = SpriteLocator()
            #print("Trying to find Sprite")
            #location = sprite_locator.locate(sprite=sprite, game_frame=game_frame)
            #print(location)
            #print("Trying to find Circle")
            #location = sprite_locator.locate(sprite=sprite_circle, game_frame=game_frame)
            #print(location)

            print("Trying to find Square")
            print(sprite_square.image_data.shape)
            location = self.find_sprite(sprite=sprite_square, game_frame=game_frame)
            print(location)

            #print("Trying to find Triangle")
            #location = sprite_locator.locate(sprite=sprite_triangle, game_frame=game_frame)
            #print(location)

        pass
