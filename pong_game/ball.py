from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QGraphicsEllipseItem

from config import ball_vel_inc


class Ball(QGraphicsEllipseItem):
    def __init__(self, parent=None):
        super(Ball, self).__init__(parent)
        self.vel_x = 0
        self.vel_y = 0

        self.setBrush(QBrush(Qt.gray))

    def reflect_x(self):
        self.vel_x = -self.vel_x
        self.vel_x += ball_vel_inc * (-1 if self.vel_x < 0 else 1)

        self.setX(self.x() + self.vel_x)

    def reflect_y(self):
        self.vel_y = -self.vel_y
        self.setY(self.y() + self.vel_y)

    def move(self):
        self.setX(self.x() + self.vel_x)
        self.setY(self.y() + self.vel_y)

    def direction(self):
        return "left" if self.vel_x < 0 else "right"
