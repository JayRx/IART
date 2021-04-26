import sys, os

import math

import pygame
import sys
import shobu
import time
from shobu.Controller.GameController import GameController
from shobu.Model.Board import Board
from shobu.Model.Game import Game
from shobu.Model.Player import Player, player_play
from shobu.MinimaxAlgorithm import *
from shobu.Model.constants import SQUARE_SIZE, BOARD_OUTLINE, WIDTH, GREEN, BLUE, \
    LIGHT_BROWN, DARK_BROWN, BOARD_PADDING, BLACK, DISPLAY_SIZE, WHITE, MoveDirect, ROWS, COLS
from shobu.View.BoardView import BoardView

from shobu.View.GameView import GameView

from shobu.Heuristics.Heuristics import *
from shobu.View.PlayerView import PlayerView
from minimax_algorithm import Minimax

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

    print(
        "3. Menu: Computer vs Computer")  # poder escolher easy, medium, hard para cada um dos dois

    print(
        "4. Import saved game state")

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
        winner = check_winner(game_controller, game, player1)
        if winner:
            run = False
            break

        player_play(game, game_view, player2, player2_view)
        winner = check_winner(game_controller, game, player2)
        if winner:
            run = False

        boards_test = game.get_boards()
        boards[1].print_all_pieces(BLACK)
        time.sleep(5)

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

    input_done = True
    while input_done:
        print("Escolha a dificuldade do computador1: 4- easy, 5- medium, 6- hard: ")
        print(

            "9. Back")
        print(
            "0. Quit")
        choice = input(" >>  ")

        if int(choice) == 4:
            difficulty = 0
            # computador1 easy/ minimax alocar
            input_done = False
        elif int(choice) == 5:
            # computador1 medium/ minimax alocar computer1
            difficulty = 1
            input_done = False
        elif int(choice) == 6:
            # computador1 hard/ minimax alocar computer1
            difficulty = 3
            input_done = False
        else:
            exec_menu(choice)
    input_done = True
    game_view = GameView(WIN)

    while run:

        time.sleep(2)
        player_play(game, game_view, player1,
                    player1_view)
        # game_view.draw_game(game)
        winner = check_winner(game_controller, game, player1)
        if winner:
            run = False
            break


        aux_game = best_move_min_p2(game, difficulty)

        game = deepcopy(aux_game)

        game_view.draw_game(game)
        winner = check_winner(game_controller, game, computer)

        game_view.draw_game(game)
        winner = check_winner(game_controller, game, player1)
        if winner:
            run = False
            break

        # Player 2 is the white player (is the ai)

        # minmaxAlgorithm = Minimax(player1, computer)
        # value, new_boards = minmaxAlgorithm.minimax(game.get_boards(), difficulty, WHITE, game_controller, float('-1000'), float('1000'))


        if winner:
            run = False

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
        "Computer1 Vs Computer2 !\n")

    input_done = True
    computer1 = None
    computer2 = None
    # Escolher em cima qual minimax queremos pruning ou não para cada um deles

    # identifies game mode
    mode = 3
    # identifies player turn
    player_turn = "BLACK"

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
    player2 = Player(WHITE, (boards[0], boards[1]))

    game = Game(boards, player1, player2)

    game_view = GameView(WIN)

    player1_view = PlayerView(WIN)
    player2_view = PlayerView(WIN)
    game_view = GameView(WIN)

    game_controller = GameController(game, game_view)

    game_controller.start()
    difficulty = 0
    difficulty2 = 0
    input_done = True
    while input_done:
        print("Escolha a dificuldade do computador1: 4- easy, 5- medium, 6- hard: ")
        print(

            "9. Back")
        print(
            "0. Quit")
        choice = input(" >>  ")

        if int(choice) == 4:
            difficulty = 1
            # computador1 easy/ minimax alocar
            input_done = False
        elif int(choice) == 5:
            # computador1 medium/ minimax alocar computer1
            difficulty = 2
            input_done = False
        elif int(choice) == 6:
            # computador1 hard/ minimax alocar computer1
            difficulty = 3
            input_done = False
        else:
            exec_menu(choice)
    input_done = True

    while input_done:
        print("Escolha a dificuldade do computador2: 4- easy, 5- medium, 6- hard: ")
        print(

            "9. Back")
        print(
            "0. Quit")
        choice = input(" >>  ")

        if int(choice) == 4:
            difficulty2 = 1
            # computador1 easy/ minimax alocar
            input_done = False
        elif int(choice) == 5:
            # computador1 medium/ minimax alocar computer1
            difficulty2 = 2
            input_done = False
        elif int(choice) == 6:
            # computador1 hard/ minimax alocar computer1
            difficulty2 = 3
            input_done = False
        else:
            exec_menu(choice)
    input_done = True

    minmaxAlgorithm = Minimax(player1, player2)
    minmaxAlgorithm2 = Minimax(player2, player1)

    while run:

        game_view = GameView(WIN)

        # Player 2 is the white player (is the ai)

        game_view.draw_game(game)
        time.sleep(10)

        value, new_boards = minmaxAlgorithm.minimax(game.get_boards(), difficulty, BLACK, game_controller, -1000, 1000)
        time.sleep(1)
        game.ai_movement(new_boards)
        # print("This is the no. of iterations of the minimax: " + str(globals.it))
        # time.sleep(10)
        game_view.draw_game(game)
        winner = check_winner(game_controller, game, player1)
        if winner:
            run = False
            break
        
        player_turn = "WHITE"

        print("Click to continue playing...(If you quit, game state is saved in text)\n")
        action = game_view.get_next_command(pygame.mouse.get_pos())
        if (action == Action.Quit):
            print("Saving...")

            game_view.export_game_state(game, mode, player_turn)

            pygame.quit()
            sys.exit()  # se clicamos para sair do jogo
        else:
            print("Resuming...\n")

        value_pl2, new_boards_pl2 = minmaxAlgorithm2.minimax(game.get_boards(), difficulty2, WHITE, game_controller,
                                                             float('-inf'), float('inf'))
        time.sleep(1)

        game.ai_movement(new_boards_pl2)
        game_view.draw_game(game)
        time.sleep(10)
        winner = check_winner(game_controller, game, player2)
        if winner:
            run = False
        
        boards_test = game.get_boards()
        boards[2].print_all_board()
        time.sleep(5)

        player_turn = "BLACK"

    print(

        "9. Back")
    print(
        "0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
    return


# Menu 4
def menu4():
    input_done = True
    print(
        "Saved game state !\n")

    while input_done:
        print(
            "Are you sure you want to import the saved game state? (Filename 'save.txt' in root) Y/N"
            )
        choice = input(" >>  ")

        ch = choice.lower()
        if ch != 'y' and ch != 'n':
            print(
                "Invalid selection, please try again.\n")
            menu_actions['main_menu']()
        elif ch == 'n':
            input_done = False
        elif ch == 'y':
            print("Trying to import 'save.txt'...\n")

            # read of the file
            try:
                save_file = open("save.txt", "r")

                # import of game structures

                valid_board = True

                for line in save_file:
                    #print(line)

                    # read game mode
                    if (line == "mode\n"):
                        print("Li o mode!\n")
                        mode_content = save_file.readline()
                        print(mode_content)
                        if mode_content == "1\n":
                            print("Hello ladies and gentlemen!\n")
                        elif mode_content == "2\n":
                            print("Hello lasse!\n")
                        elif mode_content == "3\n":
                            print("Are you robots?!\n")

                    # read player turn
                    elif (line == "player_turn\n"):
                        print("Li o player_turn!\n")
                        player_content = save_file.readline()
                        print(player_content)
                        if player_content == "BLACK\n":
                            print("Hello player1!\n")
                        elif player_content == "WHITE\n":
                            print("Hello player 2!\n")
                    
                    # read board
                    elif (line == "board\n"):
                        print("Li o board!\n")
                        valid_board = True

                        # 4 boards
                        for board_index in range(4):
                            # each board has 16 cells    
                            for board_cell in range(16):
                                inner_content = save_file.readline()
                                if (inner_content == "0\n"):
                                    print("blank cell\n")
                                elif (inner_content == "(0, 0, 0)\n"):
                                    print("black piece\n")
                                elif (inner_content == "(255, 255, 255)\n"):
                                    print("white piece\n")
                                else:
                                    print("invalid board content\n")
                                    valid_board = False
                                    break
                            if not valid_board:
                                print("file reading aborted! In board index: " + str(board_index))
                                break
                            print(str(board_index) + " board line added!")

                # load game state
                

                save_file.close()
                

                if valid_board:
                    print("Game state imported!!!\n")

            except FileNotFoundError:
                print("There isn't a game save in the root!\n")

            input_done = False

    input_done = True


            

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
    '4': menu4,

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


def check_winner(game_controller, game, player):
    res = game_controller.objective_test(game.get_boards(), player)
    if res == -1:
        print("game isn't over!")
        return False
    elif res == 1 or res == 2:
        if player.get_color == BLACK:
            player_color = "Black"
        else:
            player_color = "White"

        print("GAME OVER! " + str(player_color) + " player wins!")
        return True
