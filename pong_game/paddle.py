import enum

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QGraphicsRectItem

from config import paddle_vel, paddle_shape, paddle_height_reduction, paddle_min_height


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

    def __init__(self, scene_h, x, parent=None):
        super(Paddle, self).__init__(parent)
        self.min = None
        self.max = None
        self.state = None
        self.vel = 0
        self.x = x
        self.scene_h = scene_h

        self.reset()

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
        self.vel = 0
        w, h = paddle_shape
        y = self.scene_h - h / 2

        self.update_rect(self.x, y, w, h)
        self.set_state(State.inactive)
        self.setY(0)

    def update_color(self):
        self.setBrush(QBrush(self.state.color()))

    def set_state(self, state):
        self.state = state
        self.update_color()

    def reduce_height(self):
        rect = self.rect()
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()

        red = paddle_height_reduction if h - paddle_height_reduction > paddle_min_height else 0

        self.update_rect(x, y + red / 2, w, h - red)

    def update_rect(self, x, y, w, h):
        self.max = (self.scene_h - h) / 2
        self.min = -self.max

        self.setRect(x, y, w, h)
