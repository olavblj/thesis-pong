from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGraphicsTextItem


class TextBox(QGraphicsTextItem):
    def __init__(self, x, y, size=None, color=None, **kwargs):
        super().__init__()
        self.x = x
        self.y = y
        self.w = self.boundingRect().width()
        self.h = self.boundingRect().height()

        for (attr, val) in kwargs.items():
            setattr(self, attr, val)

        if color is not None:
            self.setDefaultTextColor(color)

        if size is not None:
            font = QFont()
            font.setPointSize(size)
            self.setFont(font)

        self.update_pos()

    def set_text(self, p_str):
        self.setPlainText(p_str)
        self.w = self.boundingRect().width()
        self.h = self.boundingRect().height()

        self.update_pos()

    def update_pos(self):
        self.setPos(self.x - self.w / 2, self.y - self.h / 2)
