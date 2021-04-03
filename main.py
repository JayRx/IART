import math

import pygame
import time
import sys

from shobu.Model.Menu import Menu, main_menu

from shobu.Heuristics.Heuristics import *
from shobu.View.PlayerView import PlayerView
from minimax_algorithm import Minimax



FPS = 60

WIN = pygame.display.set_mode((DISPLAY_SIZE, DISPLAY_SIZE))  # Display game

pygame.display.set_caption('Shobu')


def main():
    main_menu()


    FPS = 60

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
    ai = True   # change this to play humanVShuman

    while run:

        game_view = GameView(WIN)
        player_play(game, game_view, player1,
                    player1_view)
        check_winner(game_controller, game, player1)

        # Player 2 is the white player (is the ai)  (maybe implement + change player?)
        if (ai == True):
            minmaxAlgorithm = Minimax(player1, player2)
            value, new_boards = minmaxAlgorithm.minimax(game.get_boards(), 1, WHITE, game_controller, float('-inf'), float('inf'))
            time.sleep(1)
            game.ai_movement(new_boards)
            check_winner(game_controller, game, player2)
        else:
            player_play(game, game_view, player2, player2_view)
            check_winner(game_controller, game, player2)


def check_winner(game_controller, game, player):
    res = game_controller.objective_test(game.get_boards(), player)
    if res == -1:
        print("game isn't over!")
    else:
        print("GAME OVER!")

main()
