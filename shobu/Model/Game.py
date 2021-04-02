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

# check if Flávio has created one
    def obtain_opposite_color_boards(self, color_board_played):
        board_diff_color = []
        for board in self.__boards:
            if board.get_color() != color_board_played:
                board_diff_color.append(board)
        return board_diff_color
