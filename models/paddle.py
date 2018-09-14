from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QGraphicsRectItem

from config import paddle_vel, PaddleColor, paddle_shape


class Paddle(QGraphicsRectItem):
    def __init__(self, scene_h, x, parent=None):
        super(Paddle, self).__init__(parent)
        self.vel = 0
        self.set_color("gray")

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
        print("reset paddle")
        self.setY((self.max - self.min) / 2)
        self.vel = 0

    def set_color(self, color):
        if color == "moving":
            self.setBrush(QBrush(PaddleColor.moving))
        elif color == "done_moving":
            self.setBrush(QBrush(PaddleColor.done_moving))
        elif color == "inactive":
            self.setBrush(QBrush(PaddleColor.inactive))
