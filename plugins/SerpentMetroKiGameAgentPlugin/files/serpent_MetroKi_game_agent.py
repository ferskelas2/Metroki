import serpent.game_agent
import serpent.input_controller

class SerpentMetroKiGameAgent(serpent.game_agent.GameAgent):

    def __init__(self, **kwargs):

        #IDENTIFY MINI METRO
        kwargs["platform"] = "steam"

        kwargs["window_name"] = "Mini Metro"

        kwargs["app_id"] = "287980"
        kwargs["app_args"] = None



        super().__init__(**kwargs)

        self.frame_handlers["PLAY"] = self.handle_play

        self.frame_handler_setups["PLAY"] = self.setup_play

    def setup_play(self):
        self.input_controller.click_string('Spielen')
        pass

    def handle_play(self, game_frame):
        print('Hello World')


        self.input_controller.tap_key(KeyboardKey.KEY_RIGHT)
        pass



    handle_play
