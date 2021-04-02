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

    def get_all_pieces(self, player_color):
        pieces = []
        for board in self.__boards:
            for row in range(ROWS):
                for col in range(COLS):
                    if (board.get_board_info()[row][col] != 0) :
                        current_piece = board.get_board_info()[row][col] 
                        if (current_piece.get_color() == player_color):
                            pieces.append(current_piece)
        return pieces
