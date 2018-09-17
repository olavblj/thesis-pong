from PyQt5.QtWidgets import QWidget, QStackedWidget, QFormLayout, QLineEdit, QPushButton, QMainWindow, QComboBox, \
    QLabel, QCheckBox, QBoxLayout, QListWidget

from config import window_size
from models.person import Person
from pong_game.solo_mode import SoloMode
from system_manager import SystemManager
from utils.utils import fetch_highscore

sys_manager = SystemManager.get_instance()


class MainWindow(QMainWindow):
    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)

        self.comps = dict()

        self.setFixedSize(*window_size)
        self.setWindowTitle('Pong')

        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        self.highscore_list = QListWidget()

        self.pong_game = SoloMode()
        self.pong_game.finished_signal.connect(self.finish_game)

        self.home_view = QWidget()
        self.pong_view = self.pong_game.scene_view.view

        self.setup_home_view()

        self.stack.addWidget(self.home_view)
        self.stack.addWidget(self.pong_view)

        self.stack.setCurrentWidget(self.home_view)

    # noinspection PyArgumentList
    def setup_home_view(self):
        res = QWidget()
        box_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        form = QWidget()
        form_layout = QFormLayout()

        self.comps["status"] = QLabel()
        self.comps["status"].setText("False")
        self.comps["status"].setStyleSheet('background-color: red')
        form_layout.addRow("Receiving", self.comps["status"])

        self.comps["name"] = QLineEdit()
        form_layout.addRow("Full Name", self.comps["name"])

        self.comps["age"] = QLineEdit()
        form_layout.addRow("Age", self.comps["age"])

        self.comps["gender"] = QComboBox()
        self.comps["gender"].addItems(["male", "female", "other"])
        form_layout.addRow("Gender", self.comps["gender"])

        self.comps["is_real"] = QCheckBox()
        form_layout.addRow("Real data", self.comps["is_real"])

        button = QPushButton("Play Solo")
        button.clicked.connect(self.play_solo)
        form_layout.addRow("", button)
        form.setLayout(form_layout)

        box_layout.addWidget(form, stretch=2)

        self.highscore_list.addItems(fetch_highscore())

        box_layout.addWidget(self.highscore_list, stretch=1)

        res.setLayout(box_layout)
        res.setFixedSize(*window_size)
        self.home_view = res

    def finish_game(self):
        self.pong_game.stop()
        self.stack.setCurrentWidget(self.home_view)
        self.update_highscore_list()

    def play_solo(self):
        name = self.comps["name"].text()
        age = self.comps["age"].text()
        gender = self.comps["gender"].currentText()

        if not name:
            name = "Olav Ljosland"

        if not age:
            age = "24"

        sys_manager.person = Person.create_or_fetch(name, age, gender)
        sys_manager.is_real_data = bool(self.comps["is_real"].checkState())

        self.stack.setCurrentWidget(self.pong_view)
        self.pong_game.start()

    def update_status_indicator(self, receiving_samples):
        self.comps["status"].setText(str(receiving_samples))
        if receiving_samples:
            self.comps["status"].setStyleSheet('background-color: green')
        else:
            self.comps["status"].setStyleSheet('background-color: red')

    def update_highscore_list(self):
        self.highscore_list.clear()
        self.highscore_list.addItems(fetch_highscore())
