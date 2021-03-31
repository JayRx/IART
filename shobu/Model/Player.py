from shobu.Model.constants import ROWS, COLS
from shobu.Model.Board import Board


class Player:

    def __init__(self, color):
        self.__win_state = False
        self.__color = color
        self.__moves = []
        self.__aggressive_moves = []
        self.__row = 0
        self.__col = 0

    def get_state(self):
        return self.__win_state

    def calc_moves2(self, board, piece):
        self.__moves = []
        self.__row = piece.get_row()
        self.__col = piece.get_col()
        for i in range(2):
            # LEFT
            if self.__row > i:
                self.__moves.append([self.__row - 1 - i, self.__col])

            # RIGHT
            if self.__row < ROWS - 1 - i:
                self.__moves.append([self.__row + 1 + i, self.__col])

            # DOWN
            if self.__col > i:
                self.__moves.append([self.__row, self.__col - 1 - i])

            # UP
            if self.__col < COLS - 1 - i:
                self.__moves.append([self.__row, self.__col + 1 + i])

            # LEFT DOWN
            if self.__row > i and self.__col > i:
                self.__moves.append([self.__row - 1 - i, self.__col - 1 - i])

            # RIGHT DOWN
            if self.__row < ROWS - 1 - i and self.__col > i:
                self.__moves.append([self.__row + 1 + i, self.__col - 1 - i])

            # LEFT UP
            if self.__row > i and self.__col < COLS - 1 - i:
                self.__moves.append([self.__row - 1 - i, self.__col + 1 + i])

            # RIGHT UP
            if self.__row < ROWS - 1 - i and self.__col < COLS - 1 - i:
                self.__moves.append([self.__row + 1 + i, self.__col + 1 + i])

        aux_moves = self.__moves.copy()  # evita algum valor ser ignorado , quando removemos vários elementos
        for move in self.__moves:
            # imp_moves = []
            move_row, move_col = move
            cell = board.get_cell(move_row, move_col)
            if cell != 0 and self.get_color() != cell.get_color():
                continue

            elif cell != 0 and self.get_color() == cell.get_color():

                aux_moves.remove(move)
        self.__moves = aux_moves
        # Verificar movimentos impossíveis por terem uma peça antes à frente
        return self.__moves

    def calc_moves(self, board, piece):
        self.__moves = []
        self.__row = piece.get_row()
        self.__col = piece.get_col()
        for i in range(2):
            # LEFT
            if self.__row > i:
                if i == 1:
                    if board.get_cell(self.__row - i, self.__col) == 0:
                        self.__moves.append([self.__row - 1 - i, self.__col])
                else:
                    self.__moves.append([self.__row - 1 - i, self.__col])

            # RIGHT
            if self.__row < ROWS - 1 - i:
                if i == 1:
                    if board.get_cell(self.__row + i, self.__col) == 0:
                        self.__moves.append([self.__row + 1 + i, self.__col])
                else:
                    self.__moves.append([self.__row + 1 + i, self.__col])

            # DOWN
            if self.__col > i:
                if i == 1:
                    if board.get_cell(self.__row, self.__col - i) == 0:
                        self.__moves.append([self.__row, self.__col - 1 - i])
                else:
                    self.__moves.append([self.__row, self.__col - 1 - i])

            # UP
            if self.__col < COLS - 1 - i:
                if i == 1:
                    if board.get_cell(self.__row, self.__col + i) == 0:
                        self.__moves.append([self.__row, self.__col + 1 + i])
                else:
                    self.__moves.append([self.__row, self.__col + 1 + i])

            # LEFT DOWN
            if self.__row > i and self.__col > i:
                if i == 1:
                    if board.get_cell(self.__row - i, self.__col - i) == 0:
                        self.__moves.append([self.__row - 1 - i, self.__col - 1 - i])
                else:
                    self.__moves.append([self.__row - 1 - i, self.__col - 1 - i])

            # RIGHT DOWN
            if self.__row < ROWS - 1 - i and self.__col > i:
                if i == 1:
                    if board.get_cell(self.__row + i, self.__col - i) == 0 and i == 2:
                        self.__moves.append([self.__row + 1 + i, self.__col - 1 - i])
                else:
                    self.__moves.append([self.__row + 1 + i, self.__col - 1 - i])

            # LEFT UP
            if self.__row > i and self.__col < COLS - 1 - i:
                if i == 1:
                    if board.get_cell(self.__row - i, self.__col + i) == 0:
                        self.__moves.append([self.__row - 1 - i, self.__col + 1 + i])
                else:
                    self.__moves.append([self.__row - 1 - i, self.__col + 1 + i])

            # RIGHT UP
            if self.__row < ROWS - 1 - i and self.__col < COLS - 1 - i:
                if i == 1:
                    if board.get_cell(self.__row + i, self.__col + i) == 0:
                        self.__moves.append([self.__row + 1 + i, self.__col + 1 + i])
                else:
                    self.__moves.append([self.__row + 1 + i, self.__col + 1 + i])

        aux_moves = self.__moves.copy()  # evita algum valor ser ignorado , quando removemos vários elementos
        for move in self.__moves:
            # imp_moves = []
            move_row, move_col = move
            cell = board.get_cell(move_row, move_col)
            if cell != 0:
                # imp_moves.append(move.copy())
                aux_moves.remove(move)
        self.__moves = aux_moves
        # Verificar movimentos impossíveis por terem uma peça antes à frente
        return self.__moves

    def set_selected_piece_pos(self, piece):
        self.__row = piece.get_row()
        self.__col = piece.get_col()

    def agr_move_cal(self, board_to_play, vector_move, piece_to_move):
        moves = self.calc_moves2(board_to_play, piece_to_move)

        result_moves = []

        for move in moves:
            if (piece_to_move.get_row() + vector_move[0]) == move[0] and (piece_to_move.get_col() + vector_move[1]) == \
                    move[1]:
                result_moves.append(move)

        self.__aggressive_moves = result_moves

    def get_color(self):
        return self.__color

    def get_moves(self):
        return self.__moves

    def get_agressive_moves(self):
        return self.__aggressive_moves
