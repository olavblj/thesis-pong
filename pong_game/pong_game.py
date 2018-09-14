import enum
import random
import time

from PyQt5.QtCore import QTimer, pyqtSignal, QObject

from config import init_ball_vel, timer_delay, paddle_shape, ball_shape, ball_radius, mid_text_size, \
    score_text_size, \
    scene_margin, Key
from pong_game.ball import Ball
from pong_game.paddle import Paddle
from pong_game.scene_and_view import SceneAndView
from pong_game.text_box import TextBox
from system_manager import SystemManager

sys_manager = SystemManager.get_instance()


class State(enum.Enum):
    inactive = 0
    countdown = 1
    playing = 2
    game_over = 3


class PongGame(QObject):
    finished_signal = pyqtSignal()
    init_score = [0, 0]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene_view = SceneAndView()

        scene_w = self.scene_view.view.sceneRect().width()
        scene_h = self.scene_view.view.sceneRect().height()

        self.boundary = [scene_w, scene_h]

        self.state = State.inactive
        self.countdown_time = None
        self.score = self.init_score

        # Create ball and paddles
        self.ball = Ball()
        self.ball.setRect((scene_w - ball_radius) / 2, scene_h - ball_radius / 2, *ball_shape)

        self.paddles = dict()
        self.paddles["left"] = Paddle(scene_h, 0)
        self.paddles["right"] = Paddle(scene_h, scene_w - paddle_shape[0] - scene_margin)

        # Lines
        self.scene_view.scene.addLine(scene_w / 2, scene_h / 2, scene_w / 2, scene_h * 2)
        self.scene_view.scene.addLine(0, scene_h, scene_w, scene_h)

        # Ball and paddles are added to the scene
        self.scene_view.scene.addItem(self.ball)
        self.scene_view.scene.addItem(self.paddles["left"])
        self.scene_view.scene.addItem(self.paddles["right"])

        # Text boxes

        self.text_boxes = dict()
        self.text_boxes["score"] = TextBox(scene_w / 2, scene_h * 0.6, size=score_text_size)
        self.scene_view.scene.addItem(self.text_boxes["score"])

        self.text_boxes["mid"] = TextBox(scene_w / 2, scene_h, size=mid_text_size)
        self.scene_view.scene.addItem(self.text_boxes["mid"])

        self.setup_connections()

        self.timer = QTimer(self.scene_view.view)
        self.timer.timeout.connect(self.main_loop)

    # <--- SETUP --->

    def setup_connections(self):
        self.scene_view.view.key_press.connect(self.handle_key_press)
        self.scene_view.view.key_release.connect(self.handle_key_release)

    # <--- GAME FLOW --->

    def main_loop(self):
        if self.state == State.countdown:
            self.loop_countdown()
        elif self.state == State.playing:
            self.loop_playing()
        elif self.state == State.game_over:
            self.loop_game_over()

    def loop_countdown(self):
        if time.time() - self.countdown_time < 3:
            mid_text_str = str(3 - int(time.time() - self.countdown_time))
        else:
            self.state = State.playing
            mid_text_str = ""

        self.text_boxes["mid"].set_text(mid_text_str)

    def loop_playing(self):
        if self.ball_hits_boundary():
            self.ball.reflect_y()
        elif self.ball_hits_paddle():
            self.ball.reflect_x()
        elif self.ball_missed() is not None:
            if self.ball_missed() == 'left':
                self.score[1] += 1
                self.serve(True)
            elif self.ball_missed() == 'right':
                self.score[0] += 1
                self.serve(False)
            self.update_score()
        else:
            self.ball.move()

        self.paddles["left"].move()
        self.paddles["right"].move()

    def loop_game_over(self):
        pass

    # <--- KEY EVENTS --->

    def handle_key_press(self, event):
        key = event.key()
        if self.state == State.playing:
            if key == Key.left_up:
                self.paddles["left"].start_up()
            elif key == Key.left_down:
                self.paddles["left"].start_down()
            elif key == Key.right_up:
                self.paddles["right"].start_up()
            elif key == Key.right_down:
                self.paddles["right"].start_down()
        elif self.state == State.game_over:
            if key == Key.replay:
                self.start()
            elif key == Key.exit:
                self.finished_signal.emit()

    def handle_key_release(self, event):
        key = event.key()
        if key in [Key.left_up, Key.left_down]:
            self.paddles["left"].stop()
        elif key in [Key.right_up, Key.right_down]:
            self.paddles["right"].stop()

    # <--- ACTION METHODS --->

    def start(self):
        sys_manager.start_recording()
        self.state = State.countdown
        self.countdown_time = time.time()
        self.reset()

    def stop(self):
        self.timer.stop()

    def game_over(self):
        self.countdown_time = time.time()
        self.state = State.game_over

        self.text_boxes["mid"].set_text("GAME OVER")
        self.text_boxes["game_over_help"] = TextBox(self.boundary[0] / 2, self.boundary[1] * 1.1,
                                                    size=mid_text_size * 0.5)
        self.scene_view.scene.addItem(self.text_boxes["game_over_help"])
        self.text_boxes["game_over_help"].set_text("Press Space to play again. Esc to go to the menu.")

        sys_manager.stop_recording()

    def reset(self):
        self.remove_text_box("game_over_help")

        self.paddles["right"].reset()
        self.paddles["left"].reset()

        self.score = self.init_score
        self.update_score()
        self.serve(random.choice([0, 1]))

    # <--- HELPER METHODS --->

    def update_score(self):
        message = str(self.score[0]) + '    ' + str(self.score[1])
        self.text_boxes["score"].set_text(message)

    def serve(self, left_side):
        self.ball.setPos(0, 0)
        self.ball.vel_y = random.choice([-3, -2, -1, 1, 2, 3])
        self.ball.vel_x = init_ball_vel * (-1 if left_side else 1)
        self.timer.start(timer_delay)

    def ball_hits_paddle(self):
        z = self.scene_view.scene.collidingItems(self.ball)
        if self.ball.collidesWithItem(self.paddles["left"]):
            return True
        elif self.ball.collidesWithItem(self.paddles["right"]):
            return True

    def ball_hits_boundary(self):
        if self.ball.y() < -self.boundary[1] / 2 + 15 or self.ball.y() > self.boundary[1] / 2 - 15:
            return True

    def ball_missed(self):
        if self.ball.x() < -self.boundary[0] / 2:
            return 'left'
        elif self.ball.x() > self.boundary[0] / 2:
            return 'right'
        else:
            return None

    def remove_text_box(self, key):
        if key in self.text_boxes:
            self.scene_view.scene.removeItem(self.text_boxes[key])
            del self.text_boxes[key]
