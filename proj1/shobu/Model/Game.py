from shobu.Model.constants import ROWS, COLS
class Game:
    def __init__(self, boards, player1, player2):
        self.__boards = boards
        self.__player1 = player1
        self.__player2 = player2
        self.__is_finish = False

    def get_player1(self):
        return self.__player1

    def get_player2(self):
        return self.__player2

    def get_boards(self):
        return self.__boards

    def get_is_finish(self):
        return self.__is_finish

    def ai_movement(self, boards):
        self.__boards = boards
        # player1_boards = boards[2], boards[3]
        # player2_boards = boards[0], boards[1]
        # self.__player1.set_boards(player1_boards)
        # self.__player2.set_boards(player2_boards)
