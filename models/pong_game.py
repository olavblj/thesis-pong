import enum
import random
import time

from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGraphicsTextItem

from config import init_ball_vel, timer_delay, paddle_shape, mid_text_size
from models.ball import Ball
from models.paddle import Paddle
from models.scene_and_view import SceneAndView


class State(enum.Enum):
    countdown = 0
    playing = 1
    game_over = 2


class PongGame:
    finished_signal = pyqtSignal()

    def __init__(self, parent=None):
        self.scene_view = SceneAndView()

        self.state = State.countdown
        self.countdown_time = None

        self.ball = Ball()
        self.ball.setRect((self.scene_view.view.size().width() - 15) / 2, self.scene_view.view.height(),
                          self.ball.radius,
                          self.ball.radius)

        self.boundary = [self.scene_view.view.width(), self.scene_view.view.height()]
        print(self.boundary)

        self.paddle_left = Paddle(self.scene_view.view.height())
        self.paddle_left.setRect(0, self.scene_view.view.size().height() / 2, *paddle_shape)

        self.paddle_right = Paddle(self.scene_view.view.height())
        self.paddle_right.setRect(self.scene_view.view.size().width() - paddle_shape[0] * 1.5,
                                  self.scene_view.view.size().height() / 2,
                                  *paddle_shape)
        self.score = [0, 0]
        self.scene_view.scene.addLine(self.boundary[0] / 2, self.boundary[1] / 2, self.boundary[0] / 2,
                                      self.boundary[1] * 2)

        self.score_text = QGraphicsTextItem()
        self.scene_view.scene.addItem(self.score_text)
        self.update_score()
        self.score_text.setPos(self.boundary[0] / 2 - self.score_text.boundingRect().width() * .85,
                               self.boundary[1] / 2)

        self.mid_text = QGraphicsTextItem()
        self.scene_view.scene.addItem(self.mid_text)
        mid_text_font = QFont()
        mid_text_font.setPointSize(mid_text_size)
        self.mid_text.setFont(mid_text_font)
        self.mid_text.setPos(self.boundary[0] / 2 - self.mid_text.boundingRect().width() / 2,
                             self.boundary[1])

        # ball and paddles are added to the scene
        self.scene_view.scene.addItem(self.ball)
        self.scene_view.scene.addItem(self.paddle_left)
        self.scene_view.scene.addItem(self.paddle_right)

        self.setup_connections()

        self.timer = QTimer(self.scene_view.view)
        self.timer.timeout.connect(self.main_loop)

    # <--- SETUP --->

    def setup_connections(self):
        self.scene_view.view.left_up_press.connect(self.paddle_left.start_up)
        self.scene_view.view.left_down_press.connect(self.paddle_left.start_down)
        self.scene_view.view.left_key_release.connect(self.paddle_left.stop)

        self.scene_view.view.right_up_press.connect(self.paddle_right.start_up)
        self.scene_view.view.right_down_press.connect(self.paddle_right.start_down)
        self.scene_view.view.right_key_release.connect(self.paddle_right.stop)

    # <--- GAME FLOW --->

    def main_loop(self):
        if self.state == State.countdown:
            self.loop_countdown()
        elif self.state == State.playing:
            self.loop_playing()
        elif self.state == State.game_over:
            self.loop_game_over()

    def loop_countdown(self):
        if self.countdown_time is None:
            self.countdown_time = time.time()
            mid_text_str = str(3 - int(time.time() - self.countdown_time))
        elif time.time() - self.countdown_time < 3:
            mid_text_str = str(3 - int(time.time() - self.countdown_time))
        else:
            self.state = State.playing
            mid_text_str = ""

        self.mid_text.setPlainText(mid_text_str)

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

        self.paddle_left.move()
        self.paddle_right.move()

    def loop_game_over(self):
        self.mid_text.setPlainText("GAME OVER: {}".format(self.score))

        if time.time() - self.countdown_time > 5:
            self.finished_signal.emit()

    # <--- ACTION METHODS --->

    def start(self):
        self.reset()

    def stop(self):
        self.timer.stop()

    def game_over(self):
        self.countdown_time = time.time()
        self.state = State.game_over

    def reset(self):
        self.score = [0, 0]
        self.serve(random.choice([0, 1]))

    # <--- HELPER METHODS --->

    def update_score(self):
        message = str(self.score[0]) + '    ' + str(self.score[1])
        self.score_text.setPlainText(message)

    def serve(self, left_side):
        self.ball.setPos(0, 0)
        self.ball.vel_y = random.choice([-3, -2, -1, 1, 2, 3])
        self.ball.vel_x = init_ball_vel * (-1 if left_side else 1)
        self.timer.start(timer_delay)

    def ball_hits_paddle(self):
        z = self.scene_view.scene.collidingItems(self.ball)
        if self.ball.collidesWithItem(self.paddle_left) or self.ball.collidesWithItem(self.paddle_right):
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
