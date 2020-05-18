import time
import os

import serpent.game_agent
import serpent.input_controller

from serpent.input_controller import KeyboardKey
from serpent.input_controller import MouseButton

from .helpers.game_status import Game
from .helpers.ppo import SerpentPPO

class SerpentMetroKiGameAgent(serpent.game_agent.GameAgent):

    def __init__(self, **kwargs):

        #IDENTIFY MINI METRO
        #kwargs["platform"] = "steam"

        #kwargs["window_name"] = "Mini Metro"

        #kwargs["app_id"] = "287980"
        #kwargs["app_args"] = None



        super().__init__(**kwargs)

        self.frame_handlers["PLAY"] = self.handle_play

        self.frame_handler_setups["PLAY"] = self.setup_play

    def setup_play(self):
        self.state = 'MM'
        self.run_count = 0


        game_inputs = {
            "Move Up": [MouseButton.LEFT],
            "Move Down": [KeyboardKey.KEY_DOWN],
            "Move Left": [KeyboardKey.KEY_LEFT],
            "Move Right": [KeyboardKey.KEY_RIGHT]
        }

        self.ppo_agent = SerpentPPO(
            frame_shape=(125, 112, 4),
            game_inputs=game_inputs
        )

        # Get last MM
        try:
            self.ppo_agent.agent.restore_model(directory=os.path.join(os.getcwd(), "datasets", "pacai"))
            self.restore_metadata()
        except Exception:
            pass


        pass

    def handle_play(self, game_frame):
        self.run_count += 1
        if self.state == 'MM':
            print('Hello World')
            self.state = 'LS'
            self.input_controller.click_screen_region(MouseButton.LEFT, "MM_Start")

        if self.state == 'LS':
            self.state = 'SP'
            self.input_controller.click_screen_region(MouseButton.LEFT, "LS_Start")

        # Save MM
        if not self.run_count % 10:
            self.ppo_agent.agent.save_model(directory=os.path.join(os.getcwd(), "datasets", "pacai", "ppo_model"),append_timestep=False)
            #self.dump_metadata()
        pass
