import os

from serpent.game import Game

from .api.api import minimetroAPI

from serpent.utilities import Singleton




class SerpentminimetroGame(Game, metaclass=Singleton):

    # 1360 x 768
    def __init__(self, **kwargs):
        kwargs["platform"] = "steam"

        kwargs["window_name"] = "Mini Metro"

        kwargs["app_id"] = "287980"
        kwargs["app_args"] = None




        super().__init__(**kwargs)

        self.api_class = minimetroAPI
        self.api_instance = None

    @property
    def screen_regions(self):
        regions = {
            "MM_Start": (245, 488, 301, 671),
            "LS_Start": (617, 1178, 664, 1331),
            "Game": (2, 69, 639, 1241)
        }

        return regions

    @property
    def sprite_paths(self):
        sprite_path = os.path.join(os.path.dirname(__file__), 'data/sprites')
        sprites = {
            'Square': os.path.join(sprite_path, 'sprite_square_0.png'),
            'Circle': os.path.join(sprite_path, 'sprite_circle_0.png'),
            'Triangle': os.path.join(sprite_path, 'sprite_triangle_0.png'),
        }

        return sprites

    @property
    def ocr_presets(self):
        presets = {
            "SAMPLE_PRESET": {
                "extract": {
                    "gradient_size": 1,
                    "closing_size": 1
                },
                "perform": {
                    "scale": 10,
                    "order": 1,
                    "horizontal_closing": 1,
                    "vertical_closing": 1
                }
            }
        }

        return presets
