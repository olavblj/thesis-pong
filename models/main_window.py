from PyQt5.QtWidgets import QWidget, QStackedWidget, QFormLayout, QLineEdit, QPushButton, QMainWindow

from config import window_size
from models.solo_mode import SoloMode


class MainWindow(QMainWindow):
    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)

        self.setFixedSize(*window_size)
        self.setWindowTitle('Pong')

        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        self.home_view = QWidget()
        self.pong_game = SoloMode()
        self.pong_game.finished_signal.connect(self.finish_game)

        self.setup_home_view()

        self.stack.addWidget(self.home_view)
        self.stack.addWidget(self.pong_game.scene_view.view)

        self.stack.setCurrentWidget(self.home_view)

    def setup_home_view(self):
        res = QWidget()
        layout = QFormLayout()
        layout.addRow("Name", QLineEdit())
        layout.addRow("Age", QLineEdit())
        layout.addRow("Gender", QLineEdit())

        button = QPushButton("Play Solo")
        button.clicked.connect(self.play_solo)
        layout.addRow(button)

        res.setLayout(layout)
        res.setFixedSize(*window_size)
        self.home_view = res

    def finish_game(self):
        self.pong_game.stop()
        self.stack.setCurrentWidget(self.home_view)
        # self.stack.removeWidget(self.pong_game.scene_view.view)

    def play_solo(self):
        self.stack.setCurrentWidget(self.pong_game.scene_view.view)
        self.pong_game.start()
