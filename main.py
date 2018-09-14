import sys

from PyQt5.QtWidgets import QApplication

from pong_game.main_window import MainWindow
from system_manager import SystemManager
from utils.streamhandler import StreamHandler

sys_manager = SystemManager.get_instance()


def main():
    app = QApplication(sys.argv)

    sys_manager.game_window = MainWindow(None)
    sys_manager.streamhandler = StreamHandler("StreamHandler")

    sys_manager.streamhandler.start()
    sys_manager.game_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
