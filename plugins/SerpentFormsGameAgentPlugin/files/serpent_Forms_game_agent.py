from serpent.game_agent import GameAgent
from .helpers.sprite_helper import SpriteHelper
from .helpers.form_helper import FormHelper



class SerpentFormsGameAgent(GameAgent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.frame_handlers["PLAY"] = self.handle_play

        self.frame_handler_setups["PLAY"] = self.setup_play

        self.sprite_helper = SpriteHelper(self)
        self.form_helper = FormHelper(self)

    def setup_play(self):
        self.forms = {'Squares': [], 'Circles': [], 'Triangles': []}
        pass

    def handle_play(self, game_frame):
        square_regions = self.sprite_helper.find(path=self.game.sprite_paths['Square'], game_frame=game_frame,
                                                 ignore_regions=[])
        circle_regions = self.sprite_helper.find(path=self.game.sprite_paths['Circle'], game_frame=game_frame,
                                                 ignore_regions=[])
        triangle_regions = self.sprite_helper.find(path=self.game.sprite_paths['Triangle'], game_frame=game_frame,
                                                   ignore_regions=[])
        forms = []
        forms.extend(self.form_helper.regions_to_forms(square_regions, 'Square'))
        forms.extend(self.form_helper.regions_to_forms(circle_regions, 'Circle'))
        forms.extend(self.form_helper.regions_to_forms(triangle_regions, 'Triangle'))

        self.form_helper.connect_forms(forms)

        pass
