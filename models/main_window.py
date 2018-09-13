from PyQt5.QtWidgets import QWidget, QStackedWidget, QFormLayout, QLineEdit, QPushButton, QMainWindow

from config import window_size
from models.pong_game import PongGame
from models.solo_mode import SoloMode


class MainWindow(QMainWindow):
    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)

        self.setFixedSize(*window_size)
        self.setWindowTitle('Pong')

        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        self.home_view = None
        self.game_view = None

        self.show_home_view()

        self.stack.addWidget(self.home_view)

    def show_home_view(self):
        res = QWidget()
        layout = QFormLayout()
        layout.addRow("Name", QLineEdit())
        layout.addRow("Address", QLineEdit())

        button = QPushButton("Play 2-Player")
        button.clicked.connect(self.play_2_player)
        layout.addRow(button)

        button = QPushButton("Play Solo")
        button.clicked.connect(self.play_solo)
        layout.addRow(button)

        res.setLayout(layout)
        res.setFixedSize(*window_size)
        self.home_view = res
        self.stack.setCurrentWidget(self.home_view)

    def finish_game(self):
        self.stack.removeWidget(self.game_view.scene_view.view)
        self.show_home_view()

    def play_2_player(self):
        self.game_view = PongGame()
        self.stack.addWidget(self.game_view.scene_view.view)
        self.stack.setCurrentWidget(self.game_view.scene_view.view)
        self.game_view.finished_signal.connect()
        self.game_view.start()

    def play_solo(self):
        self.game_view = SoloMode()
        self.stack.addWidget(self.game_view.scene_view.view)
        self.stack.setCurrentWidget(self.game_view.scene_view.view)
        self.game_view.start()
