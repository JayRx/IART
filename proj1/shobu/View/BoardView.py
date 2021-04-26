from shobu.Model.constants import BLACK, WHITE, OUTLINE, ROWS, COLS, SQUARE_SIZE, BOARD_OUTLINE, BOARD_PADDING
import shobu.Model.Board
import pygame

from shobu.Model.piece import Piece
from shobu.View.PieceView import PieceView


class BoardView:

    def __init__(self):
        pass

    def draw_squares(self, board, window_game):
        for row in range(ROWS):
            for col in range(ROWS):
                pygame.draw.rect(window_game, board.get_color(), (
                    board.get_x() + (SQUARE_SIZE + BOARD_OUTLINE) * col,
                    board.get_y() + (SQUARE_SIZE + BOARD_OUTLINE) * row,
                    SQUARE_SIZE, SQUARE_SIZE))

    def draw_outline(self, board, window_game):
        for row in range(ROWS):
            for col in range(ROWS):
                pygame.draw.rect(window_game, OUTLINE,
                                 (board.get_x(), board.get_y(), board.get_background_size(),
                                  board.get_background_size()))

    """ function that draws the board """

    def draw(self, window_game, board, piece_view):
        # Desenha linhas e quadrados
        self.draw_outline(board, window_game)
        self.draw_squares(board, window_game)

        aux_board = board
        # desenhar peças
        for row in range(ROWS):
            for col in range(COLS):
                piece = aux_board.get_board_info()[row][col]
                if piece != 0:  # se é zero, não tem peça no quadrado do tabuleiro, guardados numa lista
                    piece_view.draw(window_game, aux_board.get_board_info()[row][col])
