import sys

from PyQt5.QtWidgets import QApplication

from models.main_window import MainWindow
from models.pong_game import PongGame


def run_without_stack():
    app = QApplication(sys.argv)
    w = PongGame()
    w.scene_view.view.show()
    sys.exit(app.exec_())


def run_with_stack():
    app = QApplication(sys.argv)
    window = MainWindow(None)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_with_stack()
