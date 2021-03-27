from shobu.Model.constants import PADDING, OUTLINE
import pygame
import shobu.Model.piece
from shobu.Model import piece
from shobu.Model.piece import Piece


class PieceView:

    def __init__(self):
        pass

    def draw(self, window_game, piece):
        radius = shobu.Model.constants.SQUARE_SIZE // 2 - PADDING
        pygame.draw.circle(window_game, piece.get_color(), (piece.get_x_in_board(), piece.get_y_in_board()), radius)
