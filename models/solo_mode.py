from models.pong_game import PongGame, State


class SoloMode(PongGame):
    def __init__(self):
        super().__init__()

        self.score = [0]
        self.update_score()

        self.action_count = 0

    # <--- SETUP --->

    def setup_connections(self):
        self.scene_view.view.right_up_press.connect(self.handle_up_press)
        self.scene_view.view.right_down_press.connect(self.handle_down_press)
        self.scene_view.view.right_key_release.connect(self.handle_release)

    # <--- GAME FLOW --->

    def loop_playing(self):
        if self.action_count == 0:
            if self.ball.direction() == "left":
                self.paddle_left.set_color("moving")
                self.paddle_right.set_color("inactive")
            elif self.ball.direction() == "right":
                self.paddle_left.set_color("inactive")
                self.paddle_right.set_color("moving")
        else:
            if self.ball.direction() == "left":
                self.paddle_left.set_color("done_moving")
                self.paddle_right.set_color("inactive")
            elif self.ball.direction() == "right":
                self.paddle_left.set_color("inactive")
                self.paddle_right.set_color("done_moving")

        if self.ball_hits_boundary():
            self.ball.reflect_y()
        elif self.ball_hits_paddle():
            self.ball.reflect_x()
            self.score[0] += 1000
            self.action_count = 0
            self.update_score()
        elif self.ball_missed() is not None:
            self.game_over()
        else:
            self.ball.move()

        self.paddle_left.move()
        self.paddle_right.move()

    # <--- HELPER METHODS --->

    def update_score(self):
        message = str(self.score[0])
        self.score_text.setPlainText(message)

    def handle_up_press(self):
        if self.state == State.playing:
            if self.action_count > 0:
                self.game_over()
            ball_dir = self.ball.direction()
            if ball_dir == "left":
                self.paddle_left.start_up()
            elif ball_dir == "right":
                self.paddle_right.start_up()

    def handle_down_press(self):
        if self.state == State.playing:
            if self.action_count > 0:
                self.game_over()
            ball_dir = self.ball.direction()
            if ball_dir == "left":
                self.paddle_left.start_down()
            else:
                self.paddle_right.start_down()

    def handle_release(self):
        if self.state == State.playing:
            self.action_count += 1
            self.paddle_left.stop()
            self.paddle_right.stop()
