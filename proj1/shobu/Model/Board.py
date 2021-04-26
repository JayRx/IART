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

    def get_cell2(self, cell):
        if 0 <= cell[0] < ROWS and 0 <= cell[1] < COLS:
            return self.__board_info[cell[0]][cell[1]]
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

    def get_all_pieces(self, player_color):
        pieces = []
        
        for row in range(ROWS):
            for col in range(COLS):
                # if cell has a piece
                if (self.__board_info[row][col] != 0) :
                    current_piece = self.__board_info[row][col] 
                    if (current_piece.get_color() == player_color):
                        pieces.append(current_piece)
        return pieces

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

        if new_row > ROWS - 1 or new_row < 0 or new_col > COLS - 1 or new_col < 0:
            self.__board_info[row][col] = 0
            return False
        else:
            self.__board_info[row][col] = 0
            self.__board_info[new_row][new_col] = piece
            # Actualizar posicionamento da peça na matriz do board e no ecrã
            piece.set_cell(cell)
            self.calc_pos_piece_in_board(piece)
            return True

    def change_pieces_active(self, piece, adv_pieces, vector_move):
        print('From Board.py, Board w/ index: ' + str(self.__index))
        row, col = piece.get_cell()

        print('From Board.py, colour of chosen Piece ' + str(piece))
        # updates board w/ new piece position
        for piece_adv in adv_pieces:
            new_row = piece_adv.get_row() + vector_move[0]
            new_col = piece_adv.get_col() + vector_move[1]
            if new_row > ROWS - 1 or new_row < 0 or new_col > COLS - 1 or new_col < 0:
                self.__board_info[row][col] = 0
            else:
                self.change_piece_cell(piece, (new_row, new_col))

        row, col = row + vector_move[0], col + vector_move[1]
        self.change_piece_cell(piece, (row, col))
        return True

    def print_all_pieces(self, player_color):
        pieces = []
        
        for row in range(ROWS):
            for col in range(COLS):
                # if cell has a piece
                if (self.__board_info[row][col] != 0) :
                    current_piece = self.__board_info[row][col] 
                    if (current_piece.get_color() == player_color):
                        print(str(current_piece) + "|")

# for game state exporting
    def get_all_board_string(self):
        board = ""
        for row in range(ROWS):
            for col in range(COLS):
                    current_cell = self.__board_info[row][col] 
                    board += (str(current_cell)+"\n")
        return board                        
        
