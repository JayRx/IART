from shobu.Controller.PlayerController import PlayerController


class GameController:

    def __init__(self, game, game_view):
        self.__game = game
        self.__game_view = game_view
        self.__player1_controller = PlayerController(game, game_view)
        self.__player2_controller = PlayerController(game, game_view)

    def start(self):
        self.__game_view.draw_game()
