from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView

from config import window_size, left_up, left_down, right_up, right_down, scene_margin


class GameView(QGraphicsView, QObject):
    def __init__(self, parent=None):
        super(GameView, self).__init__(parent)

        # Set size and position
        self.setFixedSize(*window_size)
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Remove scrollbar
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setRenderHint(QPainter.Antialiasing)
        self.setSceneRect(
            self.x() - scene_margin,
            self.y() + self.height() / 2 - scene_margin,
            self.width(),
            self.height()
        )

    # Define the signals that will be passed onto the game class instance
    left_up_press = pyqtSignal()
    left_down_press = pyqtSignal()
    right_up_press = pyqtSignal()
    right_down_press = pyqtSignal()
    right_key_release = pyqtSignal()
    left_key_release = pyqtSignal()

    # Define key press events so that the signals are emitted. These signals are caught by PongGame class instance.
    def keyPressEvent(self, event):
        if event.key() == left_up:
            self.left_up_press.emit()
        elif event.key() == left_down:
            self.left_down_press.emit()
        elif event.key() == right_up:
            self.right_up_press.emit()
        elif event.key() == right_down:
            self.right_down_press.emit()

    def keyReleaseEvent(self, event):
        if event.key() in [left_up, left_down]:
            self.left_key_release.emit()
        elif event.key() in [right_up, right_down]:
            self.right_key_release.emit()
