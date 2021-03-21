import pygame
from .constants import ROWS, COLS, BLACK, WHITE, SQUARE_SIZE, BOARD_PADDING, BOARD_OUTLINE

class Piece:
    PADDING = 10
    OUTLINE = 2

    def __init__(self, row, col, color, board):
        self.row = row
        self.col = col
        self.color = color
        self.board = board
        self.board_x, self.board_y = board.get_pos()

        self.x = 0
        self.y = 0
        self.calc_pos()

        self.moves = []
        self.aggressive_moves = []

    def calc_pos(self):
        self.x = self.board_x + (SQUARE_SIZE + BOARD_OUTLINE) * self.col + SQUARE_SIZE // 2
        self.y = self.board_y + (SQUARE_SIZE + BOARD_OUTLINE) * self.row + SQUARE_SIZE // 2

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)

    def __repr__(self):
        return str(self.color)

    def calc_moves(self):
        self.moves = []
        for i in range(2):
            if self.row > i:
                self.moves.append([self.row - 1 - i, self.col])
            if self.row < ROWS - 1 - i:
                self.moves.append([self.row + 1 + i, self.col])
            if self.col > i:
                self.moves.append([self.row, self.col - 1 - i])
            if self.col < COLS - 1 - i:
                self.moves.append([self.row, self.col + 1 + i])
            if self.row > i and self.col > i:
                self.moves.append([self.row - 1 - i, self.col - 1 - i])
            if self.row < ROWS - 1 - i and self.col > i:
                self.moves.append([self.row + 1 + i, self.col - 1 - i])
            if self.row > i and self.col < COLS - 1 - i:
                self.moves.append([self.row - 1 - i, self.col + 1 + i])
            if self.row < ROWS - 1 - i and self.col < COLS - 1 - i:
                self.moves.append([self.row + 1 + i, self.col + 1 + i])

        for move in list(self.moves):
            move_row, move_col = move
            cell = self.board.get_cell(move_row, move_col)
            if cell != 0:
                self.moves.remove(move)
    
    def calc_aggressive_moves(self):    # incomplete

        self.aggressive_moves = []

        # copy from calc_moves

        for i in range(2):
            if self.row > i:
                self.aggressive_moves.append([self.row - 1 - i, self.col])
            if self.row < ROWS - 1 - i:
                self.aggressive_moves.append([self.row + 1 + i, self.col])
            if self.col > i:
                self.aggressive_moves.append([self.row, self.col - 1 - i])
            if self.col < COLS - 1 - i:
                self.aggressive_moves.append([self.row, self.col + 1 + i])
            if self.row > i and self.col > i:
                self.aggressive_moves.append([self.row - 1 - i, self.col - 1 - i])
            if self.row < ROWS - 1 - i and self.col > i:
                self.aggressive_moves.append([self.row + 1 + i, self.col - 1 - i])
            if self.row > i and self.col < COLS - 1 - i:
                self.aggressive_moves.append([self.row - 1 - i, self.col + 1 + i])
            if self.row < ROWS - 1 - i and self.col < COLS - 1 - i:
                self.aggressive_moves.append([self.row + 1 + i, self.col + 1 + i])

        # end of copy (maybe we should create a function, only for this)

        for move in list(self.moves):
            move_row, move_col = move
            cell = self.board.get_cell(move_row, move_col)
            if cell == 0:
                # removes the moves that end on a 'space' (staying only with moves that remove a stone)
                self.aggressive_moves.remove(move)

    def get_moves(self):
        return self.moves

    def get_aggressive_moves(self):
        return self.aggressive_moves

    def get_cell(self):
        return self.row, self.col

    def set_cell(self, cell):
        self.row, self.col = cell
        self.calc_pos()

    def get_color(self):
        return self.color

    def refresh_board(self, board):
        self.board = board
