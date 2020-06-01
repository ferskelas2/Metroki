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
        forms = []
        square_regions = self.sprite_helper.find(path=self.game.sprite_paths['Square'], game_frame=game_frame,
                                                 ignore_regions=[])
        squares = self.form_helper.regions_to_forms(square_regions, 'Squares', {'repeating': True})
        forms.extend(squares)
        circle_regions = self.sprite_helper.find(path=self.game.sprite_paths['Circle'], game_frame=game_frame,
                                                 ignore_regions=self.form_helper.forms_to_regions(self.forms['Circles']))
        circles = self.form_helper.regions_to_forms(circle_regions, 'Circles')
        forms.extend(circles)
        triangle_regions = self.sprite_helper.find(path=self.game.sprite_paths['Triangle'], game_frame=game_frame,
                                                   ignore_regions=self.form_helper.forms_to_regions(self.forms['Triangles']))
        triangles = self.form_helper.regions_to_forms(triangle_regions, 'Triangles')
        forms.extend(triangles)

        print(self.form_helper.forms_to_regions(forms, repeating=True))

        if len(forms) >= 2:
            self.form_helper.connect_forms(forms)
            for form in forms:
                self.forms[form.type_name].append(form)

        pass
