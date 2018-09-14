from PyQt5.QtWidgets import QWidget, QStackedWidget, QFormLayout, QLineEdit, QPushButton, QMainWindow, QComboBox, QLabel

from config import window_size
from models.person import Person
from pong_game.solo_mode import SoloMode
from system_manager import SystemManager

sys_manager = SystemManager.get_instance()


class MainWindow(QMainWindow):
    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)

        self.comps = dict()

        self.setFixedSize(*window_size)
        self.setWindowTitle('Pong')

        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        self.pong_game = SoloMode()
        self.pong_game.finished_signal.connect(self.finish_game)

        self.home_view = QWidget()
        self.pong_view = self.pong_game.scene_view.view

        self.setup_home_view()

        self.stack.addWidget(self.home_view)
        self.stack.addWidget(self.pong_view)

        self.stack.setCurrentWidget(self.home_view)

    def setup_home_view(self):
        res = QWidget()
        layout = QFormLayout()

        self.comps["status"] = QLabel()
        self.comps["status"].setText("False")
        layout.addRow("Recieving", self.comps["status"])

        self.comps["name"] = QLineEdit()
        layout.addRow("Full Name", self.comps["name"])

        self.comps["age"] = QLineEdit()
        layout.addRow("Age", self.comps["age"])

        self.comps["gender"] = QComboBox()
        self.comps["gender"].addItems(["male", "female", "other"])
        layout.addRow("Gender", self.comps["gender"])

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
        name = self.comps["name"].text()
        age = self.comps["age"].text()
        gender = self.comps["gender"].currentText()

        if not name:
            name = "Olav Ljosland"

        if not age:
            age = "24"

        sys_manager.person = Person.create_or_fetch(name, age, gender)

        self.stack.setCurrentWidget(self.pong_view)
        self.pong_game.start()

    def update_status_indicator(self, receiving_samples):
        self.comps["status"].setText(str(receiving_samples))
