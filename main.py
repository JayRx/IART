import math

import pygame
import sys

from shobu.Model.Menu import Menu, main_menu

from shobu.Heuristics.Heuristics import *
from shobu.View.PlayerView import PlayerView

FPS = 60

WIN = pygame.display.set_mode((DISPLAY_SIZE, DISPLAY_SIZE))  # Display game

pygame.display.set_caption('Shobu')


def main():
    main_menu()


""" FPS = 60

    WIN = pygame.display.set_mode((DISPLAY_SIZE, DISPLAY_SIZE))  # Display game

    pygame.display.set_caption('Shobu')

    radius = SQUARE_SIZE // 2 - 10

    run = True
    clock = pygame.time.Clock()
    clock.tick(FPS)

    boards = [Board(0, 0, DARK_BROWN, 0), Board(0, 1, LIGHT_BROWN, 1), Board(1, 0, DARK_BROWN, 2),
              Board(1, 1, LIGHT_BROWN, 3)]
    # Passive move

    player1 = Player(BLACK, (boards[2], boards[3]))
    player2 = Player(WHITE, (boards[0], boards[1]))

    game = Game(boards, player1, player2)

    game_view = GameView(WIN)

    player1_view = PlayerView(WIN)
    player2_view = PlayerView(WIN)
    game_view = GameView(WIN)

    game_controller = GameController(game, game_view)

    game_controller.start()


    while run:

        game_view = GameView(WIN)
        player_play(game, game_view, player1,
                    player1_view)

        player_play(game, game_view, player2, player2_view)

        res = game_controller.objective_test(game.get_boards(), player1)
        if res == -1:
            print("gama not over")
    """
"""piece = aux_boards[2].get_board_info()[3][2]
        player1.agr_move_cal(aux_boards[2], result[0], piece)
        aux_list = player1.get_agressive_moves()
        """
"""# aggressive mode
        moves = active_mode1(result[0], player1, aux_boards, game_view, result[1])

        vector = None
        run2 = False
        while not run2:
            aux_result = active_mode2(moves, selected_board, boards, piece, game_view, vector_move)
            run2 = aux_result[0]
            vector = aux_result[1]

        game_view.draw_game()
        pygame.display.update()

        vector = vector[0] - aux_row, vector[1] - aux_col  # vector do movimento
        return vector, selected_board.get_color()  # return vector movimento, cor do board onde foi o mov passivo
"""
"""  else:
        empty_result = []
        return empty_result

        res = game_controller.objective_test(aux_boards, player1)
        if res == -1:
            print("game isn't over!")

        heuristics.calc(aux_boards, player1)
        heuristics.print_value()

        or move in aux_list:
            row, col = move
            board_x, board_y = aux_boards[2].get_pos()
            # Transformações dos valores para desenhar tendo em conta tada a janela do jogo
            move_x = board_x + (SQUARE_SIZE + BOARD_OUTLINE) * col + SQUARE_SIZE // 2
            move_y = board_y + (SQUARE_SIZE + BOARD_OUTLINE) * row + SQUARE_SIZE // 2
            pygame.draw.circle(WIN, GREEN, (move_x, move_y), radius)
            # refresh display
        # player2
        pygame.display.update()
        result = passive_mode1(player2, player2.get_color(), radius, run, aux_boards, game_view)

        # aggressive mode
        active_mode1(run, result[0], player2.get_color(), player2, radius, aux_boards, game_view, result[1])

        res = game_controller.objective_test(aux_boards, player2)
        if res == -1:
            print("game isn't over!")
        # terminar quando for "gameover"    (testar)

        heuristics.calc(aux_boards, player2)
        heuristics.print_value()

    # passive_mode1(player2, player2.get_color(), radius, run, game.get_boards(), game_view)

"""

main()
