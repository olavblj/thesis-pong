from config import Key
from pong_game.pong_game import PongGame, State

from system_manager import SystemManager

sys_manager = SystemManager.get_instance()


class SoloMode(PongGame):
    init_score = 0

    def __init__(self):
        super().__init__()

        self.update_score()

        self.action_count = 0

    # <--- SETUP --->

    # <--- GAME FLOW --->

    def loop_playing(self):
        if self.action_count == 0:
            if self.ball.direction() == "left":
                self.paddles["left"].set_color("moving")
                self.paddles["right"].set_color("inactive")
            elif self.ball.direction() == "right":
                self.paddles["left"].set_color("inactive")
                self.paddles["right"].set_color("moving")
        else:
            if self.ball.direction() == "left":
                self.paddles["left"].set_color("done_moving")
                self.paddles["right"].set_color("inactive")
            elif self.ball.direction() == "right":
                self.paddles["left"].set_color("inactive")
                self.paddles["right"].set_color("done_moving")

        if self.ball_hits_boundary():
            self.ball.reflect_y()
        elif self.ball_hits_paddle():
            self.ball.reflect_x()
            self.score += 1000
            self.action_count = 0
            self.update_score()
        elif self.ball_missed() is not None:
            self.game_over()
        else:
            self.ball.move()

        self.paddles["left"].move()
        self.paddles["right"].move()

    # <--- ACTION METHODS --->

    def reset(self):
        super(SoloMode, self).reset()
        self.action_count = 0
        self.paddles["right"].set_color("inactive")
        self.paddles["left"].set_color("inactive")

    # <--- HELPER METHODS --->

    def update_score(self):
        message = str(self.score)
        self.text_boxes["score"].set_text(message)

    def handle_key_press(self, event):
        key = event.key()
        if self.state == State.playing:
            ball_dir = self.ball.direction()

            if key == Key.solo_up:
                sys_manager.current_action = "arm/{}".format(ball_dir)

                if self.action_count > 0:
                    self.game_over()

                self.paddles[ball_dir].start_up()
            elif key == Key.solo_down:
                sys_manager.current_action = "foot/{}".format(ball_dir)

                if self.action_count > 0:
                    self.game_over()

                self.paddles[ball_dir].start_down()

        elif self.state == State.game_over:
            if key == Key.replay:
                self.start()
            elif key == Key.exit:
                self.finished_signal.emit()

    def handle_key_release(self, event):
        key = event.key()
        if self.state == State.playing:
            if key in [Key.solo_up, Key.solo_down]:
                sys_manager.current_action = None
                self.action_count += 1
                self.paddles["left"].stop()
                self.paddles["right"].stop()
