from PyQt5.QtWidgets import QGraphicsScene

from pong_game.gameview import GameView


class SceneAndView:
    def __init__(self):
        self.scene = QGraphicsScene()
        self.view = GameView()
        self.view.setScene(self.scene)
