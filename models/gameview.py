from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView

from config import window_size, scene_margin


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

        self.pressing_key = False

        self.setSceneRect(
            self.x() - scene_margin,
            self.y() + self.height() / 2,
            self.width() - scene_margin * 2,
            self.height()
        )

    # Define the signals that will be passed onto the game class instance

    key_press = pyqtSignal(object)
    key_release = pyqtSignal(object)

    # Define key press events so that the signals are emitted. These signals are caught by PongGame class instance.
    def keyPressEvent(self, event):
        self.key_press.emit(event)

    def keyReleaseEvent(self, event):
        self.key_release.emit(event)
