"""from shobu.Controller.PlayerController import PlayerController
from shobu.View.GameView import GameView
from shobu.Model.Player import Player


class GameController:

    def __init__(self, game, game_view):
        self.__game = game
        self.__game_view = game_view
        self.__player1_controller = PlayerController(game, game_view)
        self.__player2_controller = PlayerController(game, game_view)

    def start_game(self):
        self.__game_view.draw_game(self.__game, self.__game_view.get_window_game())

        while not self.game.get_player1().get_state() and not self.game.get_player2().get_state():
"""
