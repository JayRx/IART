import pygame
from .constants import LIGHT_BROWN, DARK_BROWN, BLACK, WHITE, OUTLINE, ROWS, COLS, SQUARE_SIZE, BOARD_OUTLINE, BOARD_PADDING
from .piece import Piece

class Board:
    def __init__(self, row, col, color, index):
        self.board = []
        self.selected_piece = None
        self.black_left = self.white_left = 4
        self.row = row
        self.col = col
        self.BACKGROUND_SIZE = SQUARE_SIZE * ROWS +  BOARD_OUTLINE * (ROWS - 1)
        self.x = BOARD_PADDING * (self.col + 1) + self.col * self.BACKGROUND_SIZE
        self.y = BOARD_PADDING * (self.row + 1) + self.row * self.BACKGROUND_SIZE
        self.color = color
        self.index = index
        self.create_board()
        self.calc_moves()

    def draw_outline(self, win):
        for row in range(ROWS):
            for col in range(ROWS):
                pygame.draw.rect(win, OUTLINE, (self.x, self.y, self.BACKGROUND_SIZE, self.BACKGROUND_SIZE))

    def draw_squares(self, win):
        for row in range(ROWS):
            for col in range(ROWS):
                pygame.draw.rect(win, self.color, (self.x + (SQUARE_SIZE + BOARD_OUTLINE) * col, self.y + (SQUARE_SIZE + BOARD_OUTLINE) * row, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row == 0:
                    self.board[row].append(Piece(row, col, WHITE, self))
                elif row == 3:
                    self.board[row].append(Piece(row, col, BLACK, self))
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_outline(win)
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def get_pos(self):
        return self.x, self.y

    def get_size(self):
        return self.BACKGROUND_SIZE

    def get_index(self):
        return self.index

    def get_cell(self, row, col):
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.board[row][col]
        else:
            return None

    def get_board(self):
        return self.board

    def calc_moves(self):
        for row in range(ROWS):
            for col in range(COLS):
                cell = self.board[row][col]
                if cell != 0:
                    cell.calc_moves()
                    cell.calc_aggressive_moves()

    def change_piece_cell(self, piece, cell):
        print('From board.py, Board w/ index: ' + str(self.index))
        row, col = piece.get_cell()
        new_row, new_col = cell

        print('From board.py, colour of chosen Piece ' + str(piece))
        # updates board w/ new piece position
        self.board[row][col] = 0
        self.board[new_row][new_col] = piece
        piece.set_cell(cell)
        piece.refresh_board(self)
        self.calc_moves()
