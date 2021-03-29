import pygame
from shobu.Model.constants import BLACK, WHITE, OUTLINE, ROWS, COLS, SQUARE_SIZE, BOARD_OUTLINE, BOARD_PADDING

from shobu.Model.piece import Piece


class Board:
    def __init__(self, row, col, color, index):
        self.__board_info = []
        self.__selected_piece = None
        self.black_left = self.white_left = 4
        self.__row = row
        self.__col = col
        self.__BACKGROUND_SIZE = SQUARE_SIZE * ROWS + BOARD_OUTLINE * (ROWS - 1)
        self.__x = BOARD_PADDING * (self.__col + 1) + self.__col * self.__BACKGROUND_SIZE
        self.__y = BOARD_PADDING * (self.__row + 1) + self.__row * self.__BACKGROUND_SIZE
        self.__color = color
        self.__index = index
        self.create_board()

    def create_board(self):
        for row in range(ROWS):
            self.__board_info.append([])
            for col in range(COLS):
                if row == 0:
                    aux_piece = Piece(row, col, WHITE)
                    self.calc_pos_piece_in_board(aux_piece)

                    self.__board_info[row].append(aux_piece)

                elif row == 3:
                    aux_piece = Piece(row, col, BLACK)
                    self.calc_pos_piece_in_board(aux_piece)

                    self.__board_info[row].append(aux_piece)
                else:
                    self.__board_info[row].append(0)

    """Funções get dos atributos da classe """

    def get_pos(self):
        return self.__x, self.__y

    def get_size(self):
        return self.__BACKGROUND_SIZE

    def get_index(self):
        return self.__index

    def get_cell(self, row, col):
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.__board_info[row][col]
        else:
            return None

    def get_color(self):
        return self.__color

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_board_info(self):
        return self.__board_info

    def get_background_size(self):
        return self.__BACKGROUND_SIZE

    """ Change a piece of a board"""

    def calc_pos_piece_in_board(self, piece):
        piece.set_x_in_board(self.__x + (SQUARE_SIZE + BOARD_OUTLINE) * piece.get_col() + SQUARE_SIZE // 2)
        piece.set_y_in_board(self.__y + (SQUARE_SIZE + BOARD_OUTLINE) * piece.get_row() + SQUARE_SIZE // 2)

    """Função para mudar posição da peça na matriz representativa do board """
    def change_piece_cell(self, piece, cell):
        print('From Board.py, Board w/ index: ' + str(self.__index))
        row, col = piece.get_cell()
        new_row, new_col = cell

        print('From Board.py, colour of chosen Piece ' + str(piece))
        # updates board w/ new piece position
        self.__board_info[row][col] = 0
        self.__board_info[new_row][new_col] = piece
        #Actualizar posicionamento da peça na matriz do board e no ecrã
        piece.set_cell(cell)
        self.calc_pos_piece_in_board(piece)

