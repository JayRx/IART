from abc import ABC, abstractmethod

from copy import deepcopy
from shobu.Model.constants import Action

class State(ABC):

    def __init__(self,game):
        self.__game = game
    @abstractmethod
    def execute(self):
        pass



# class GameState:

#     def __init__(self, game):
#         super().__init__()

#         self.game_state = GameState(game)

#     def execute(self,action):

#         if action == Action.buttonDown:
#            if game.verify_piece(pos_mouse)



# class PlayerState:

#     def __init__(self,game, game_view):
#         self.__game = game
#         self.__game_view = game_view

#     def execute(self,game, game_view):


# class MenuState:

#     def __init__(self,game, game_view):
#         self.__game = game
#         self.__game_view = game_view

#     def execute(self,game, game_view):

class MinimaxState:
    def __init__(self, game, boards, possible_play_boards, pieces):
        self.__game = game
        #self.__game_view = game_view
        self.boards = boards    # all boards (untouched)
        self.possible_play_boards = possible_play_boards    #maybe need to get board index to replace it in the "real" board
        self.boards_after_play = deepcopy(self.boards)
        self.pieces = pieces
        self.compute_boards_after_play()

    def get_possible_play_passive_board(self):
        print(self.possible_play_boards)
        board_passive, board_aggressive = self.possible_play_boards
        return board_passive

    def get_possible_play_aggressive_board(self):
        board_passive, board_aggressive = self.possible_play_boards
        return board_aggressive

    def compute_boards_after_play(self):
        board_passive = self.get_possible_play_passive_board()
        board_aggressive = self.get_possible_play_aggressive_board()
        self.boards_after_play[board_passive.get_index()] = board_passive
        self.boards_after_play[board_aggressive.get_index()] = board_aggressive

    def get_boards_after_play(self):
        return self.boards_after_play
    
    #def execute(self,game, game_view):
    # def execute(self):