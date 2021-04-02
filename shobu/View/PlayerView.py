from shobu.View.GameView import GameView
from shobu.Model.Game import Game
from shobu.Model.constants import BLUE, RADIUS, SQUARE_SIZE, BOARD_OUTLINE, GREEN, RED

import pygame


class PlayerView:

    def __init__(self, window):
        self.__window = window



    # desenhar jogadas possíveis e seleção de peça
    def draw_view_piece_select(self,selected_x, selected_y, color):
        pygame.draw.circle(self.__window, color, (selected_x, selected_y), RADIUS - 10)

    def draw_passive_moves(self,board_x, board_y,player):

        for move in player.get_moves():
            row, col = move
            # Transformações dos valores para desenhar tendo em conta tada a janela do jogo
            move_x = board_x + (SQUARE_SIZE + BOARD_OUTLINE) * col + SQUARE_SIZE // 2
            move_y = board_y + (SQUARE_SIZE + BOARD_OUTLINE) * row + SQUARE_SIZE // 2
            pygame.draw.circle(self.__window, GREEN, (move_x, move_y), RADIUS - 5)

        # refresh display

        pygame.display.update()

    def draw_active_moves(self,board_x, board_y,player):
        for move in player.get_agressive_moves():
            row, col = move
            # Transformações dos valores para desenhar tendo em conta tada a janela do jogo
            move_x = board_x + (SQUARE_SIZE + BOARD_OUTLINE) * col + SQUARE_SIZE // 2
            move_y = board_y + (SQUARE_SIZE + BOARD_OUTLINE) * row + SQUARE_SIZE // 2
            pygame.draw.circle(self.__window, RED, (move_x, move_y), RADIUS - 5)

        # refresh display

        pygame.display.update()