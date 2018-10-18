import enum

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QGraphicsEllipseItem

from config import ball_vel_inc


class Direction(enum.Enum):
    left = "left"
    right = "right"

    def __str__(self):
        return self.value

    def opposite(self):
        if self == self.left:
            return Direction.right
        else:
            return Direction.left


class Ball(QGraphicsEllipseItem):
    def __init__(self, parent=None):
        super(Ball, self).__init__(parent)
        self.vel_x = 0
        self.vel_y = 0

        self.setBrush(QBrush(Qt.gray))

    def reflect_x(self, paddle_y, paddle_h):
        y = self.y()
        degree = (2 * (y - paddle_y)) / paddle_h
        self.vel_y += 3 * np.tanh(degree)

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
        return Direction.left if self.vel_x < 0 else Direction.right
