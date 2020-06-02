import itertools
import cv2
from serpent.visual_debugger.visual_debugger import VisualDebugger
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
        debugger = VisualDebugger()
        # Alle Formen Dictionary in eine Liste von Formen umwandeln
        old = [form for forms in self.forms.values() for form in forms]
        # Die wiederholenden Formen finden
        forms = []
        forms.extend(self.form_helper.get_repeating(old))
        #Alle Vierecke in dem Bild finden
        square_regions, image = self.sprite_helper.find(path=self.game.sprite_paths['Square'], game_frame=game_frame, max=1,
                                                 ignore_regions=self.form_helper.forms_to_regions(old))
        squares = self.form_helper.regions_to_forms(square_regions, 'Squares', {'repeating': True})
        forms.extend(squares)
        #Alle Kreise in dem Bild finden
        circle_regions, image = self.sprite_helper.find(path=self.game.sprite_paths['Circle'], game_frame=game_frame, max=1,
                                                 ignore_regions=self.form_helper.forms_to_regions(old))
        circles = self.form_helper.regions_to_forms(circle_regions, 'Circles')
        forms.extend(circles)
        #Alle Dreiecke in dem Bild finden
        triangle_regions, image = self.sprite_helper.find(path=self.game.sprite_paths['Triangle'], game_frame=game_frame,
                                                   max=1, ignore_regions=self.form_helper.forms_to_regions(old))
        triangles = self.form_helper.regions_to_forms(triangle_regions, 'Triangles')
        forms.extend(triangles)

        # Dem Visuellen Debugger Bild daten übergeben
        debugger.store_image_data(image_data=game_frame.frame, image_shape=game_frame.frame.shape,
                                  bucket="0")
        debugger.store_image_data(image_data=game_frame.grayscale_frame, image_shape=game_frame.grayscale_frame.shape, bucket="1")

        # Wenn zwei Formen Gefunden wurden, diese Verbinden
        if len(forms) >= 2:
            self.form_helper.connect_forms(forms)
            # Gefundene Formen abspeichern
            for form in forms:
                if form not in self.forms[form.type_name]:
                    self.forms[form.type_name].append(form)

        pass
