import enum

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QGraphicsRectItem

from config import paddle_vel, paddle_shape


class State(enum.Enum):
    inactive = 0
    moving = 1
    done_moving = 2

    def color(self):
        if self == self.inactive:
            return Qt.white
        elif self == self.moving:
            return Qt.green
        elif self == self.done_moving:
            return Qt.gray


class Paddle(QGraphicsRectItem):
    state = State.inactive

    def __init__(self, scene_h, x, parent=None):
        super(Paddle, self).__init__(parent)
        self.vel = 0
        self.set_state(State.inactive)

        self.min = 0
        self.max = scene_h - paddle_shape[1]

        w, h = paddle_shape

        self.setRect(x, scene_h / 2, w, h)

    def start_up(self):
        self.vel = -paddle_vel

    def start_down(self):
        self.vel = paddle_vel

    def stop(self):
        self.vel = 0

    def move(self):
        if self.vel != 0:
            y = self.y()
            if y + self.vel < self.min:
                self.setY(self.min)
            elif y + self.vel > self.max:
                self.setY(self.max)
            else:
                self.setY(y + self.vel)

    def reset(self):
        self.setY((self.max - self.min) / 2)
        self.vel = 0

    def update_color(self):
        self.setBrush(QBrush(self.state.color()))

    def set_state(self, state):
        self.state = state

        self.update_color()

