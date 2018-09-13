from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QGraphicsRectItem

from config import paddle_vel, PaddleColor


class Paddle(QGraphicsRectItem):
    def __init__(self, max_height, parent=None):
        super(Paddle, self).__init__(parent)
        self.max_height = max_height - 105
        self.vel = 0
        self.set_color("gray")

    def start_up(self):
        self.vel = -paddle_vel

    def start_down(self):
        self.vel = paddle_vel

    def stop(self):
        self.vel = 0

    def move(self):
        if self.vel != 0:
            y = self.y()
            if y < 0:
                self.setY(0)
            elif y > self.max_height:
                self.setY(self.max_height)
            else:
                self.setY(y + self.vel)

    def set_color(self, color):
        if color == "moving":
            self.setBrush(QBrush(PaddleColor.moving))
        elif color == "done_moving":
            self.setBrush(QBrush(PaddleColor.done_moving))
        elif color == "inactive":
            self.setBrush(QBrush(PaddleColor.inactive))
