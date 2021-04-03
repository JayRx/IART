import sys, os

import math

import pygame
import sys
import shobu
from shobu.Controller.GameController import GameController
from shobu.Model.Board import Board
from shobu.Model.Game import Game
from shobu.Model.Player import Player, player_play
from shobu.Model.constants import SQUARE_SIZE, BOARD_OUTLINE, WIDTH, GREEN, BLUE, \
    LIGHT_BROWN, DARK_BROWN, BOARD_PADDING, BLACK, DISPLAY_SIZE, WHITE, MoveDirect, ROWS, COLS
from shobu.View.BoardView import BoardView

from shobu.View.GameView import GameView

from shobu.Heuristics.Heuristics import *
from shobu.View.PlayerView import PlayerView

FPS = 60

WIN = pygame.display.set_mode((DISPLAY_SIZE, DISPLAY_SIZE))  # Display game

pygame.display.set_caption('Shobu')

menu_actions = {}


class Menu:
    pass


# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu
def main_menu():
    os.system('clear')

    print(
        "Welcome,\n")
    print(
        "Please choose the menu you want to start:")
    print(
        "1. Menu: Human vs Human")
    print(
        "2. Menu: Human vs Computer")  # poder escolher easy, medium, hard para cada um dos dois

    print("3. Menu: Computer vs Computer")  # poder escolher easy, medium, hard para cada um dos dois

    print(
        "\n0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)

    return


# Execute menu
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print(
                "Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return


# Menu 1
def menu1():
    print(
        "Human vs Human !\n")

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

    while run:

        game_view = GameView(WIN)
        player_play(game, game_view, player1,
                    player1_view)

        player_play(game, game_view, player2, player2_view)

        res = game_controller.objective_test(game.get_boards(), player1)
        if res == -1:
            print("gama not over")

    print(
        "9. Back")
    print(
        "0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
    return


# Menu 2
def menu2():
    print(
        "Human vs Computer!\n")

    # Poder escolher dificuldade para escolher algoritmo se quero Hints no jogador humano

    print(
        "Human vs Human !\n")

    FPS = 60

    WIN = pygame.display.set_mode((DISPLAY_SIZE, DISPLAY_SIZE))  # Display game

    pygame.display.set_caption('Shobu')

    run = True
    clock = pygame.time.Clock()
    clock.tick(FPS)

    boards = [Board(0, 0, DARK_BROWN, 0), Board(0, 1, LIGHT_BROWN, 1), Board(1, 0, DARK_BROWN, 2),
              Board(1, 1, LIGHT_BROWN, 3)]
    # Passive move

    player1 = Player(BLACK, (boards[2], boards[3]))
    computer = Player(WHITE, (boards[0], boards[1]))

    game = Game(boards, player1, computer)

    game_view = GameView(WIN)

    player1_view = PlayerView(WIN)
    computer_view = PlayerView(WIN)
    game_view = GameView(WIN)

    game_controller = GameController(game, game_view)

    game_controller.start()

    while run:
        game_view = GameView(WIN)
        player_play(game, game_view, player1,
                    player1_view)

    print(
        "9. Back")
    print(
        "0. Quit")

    choice = input(" >>  ")
    exec_menu(choice)
    return


# Menu 3
def menu3():
    print(
        "Hello Menu 2 !\n")
    print(
        "9. Back")
    print(
        "0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
    return


# Back to main menu
def back():
    menu_actions['main_menu']()


# Exit program
def exit():
    sys.exit()


# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '3': menu3,
    '9': back,
    '0': exit,
}

# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()
