# Python3 program to find the next optimal move for a player
from copy import deepcopy
import copy
from shobu.Model.constants import ROWS, COLS

from shobu.Heuristics.Heuristics import *
from shobu.Model.Player import *


# This is the minimax function. It considers all
# the possible ways the game can go and returns
# the value of the board
# (* Initial call *)
# minimax(origin, depth, TRUE)
# passar algo iterável
def minimax(depth, is_max_player1, game):
    heuristics = Heuristics()

    # para depth == 0 or terminal node
    if depth == 0 and is_max_player1:
        heuristics.calc(game.get_boards(), game.get_player1())
        return heuristics.get_value()
    elif depth == 0 and not is_max_player1:
        heuristics.calc(game.get_boards(), game.get_player2())
        return heuristics.get_value()

    if heuristics.objective_test(game.get_boards(), game.get_player1()) == 1:
        print("Player1 Wins")
        return heuristics.get_value()

    if heuristics.objective_test(game.get_boards(), game.get_player2()) == 2:
        print("Player2 Wins")
        return heuristics.get_value()
    # Empate?

    # If this maximizer's move
    if is_max_player1:
        best = float('-inf')

        for board in game.get_player1().get_boards():

            for row in range(ROWS):

                for col in range(COLS):
                    # Check if cell is empty
                    piece = board.get_cell(row, col)
                    save = copy.copy(game)
                    game = copy.copy(save)
                    if piece != 0 and piece.get_color() == game.get_player1().get_color():
                        # calculate and Make the possible passive moves

                        game.get_player1().calc_moves(board, piece)
                        if len(game.get_player2().get_moves()) != 0:

                            # Para cada passive move calculado, efetuar movimento
                            vector_move = []
                            color_played = board.get_color()

                            for move in game.get_player1().get_moves():

                                vector_move = move[0] - piece.get_row(), move[1] - piece.get_col()
                                # movimento passivo efetuado
                                game.get_player1().get_board(board).change_piece_cell(piece, move)

                                # Fazer agressive move

                                for board2 in game.get_boards():

                                    if board2.get_color() != color_played:

                                        for row2 in range(ROWS):

                                            for col2 in range(COLS):
                                                bef_act_game = copy.copy(game)
                                                # Check if cell is empty
                                                piece2 = board2.get_cell(row2, col2)

                                                if piece2 != 0 and piece2.get_color() == game.get_player1().get_color():

                                                    rest = game.get_player1().active_move(board2, vector_move, piece2,
                                                                                          color_played)
                                                    if len(game.get_player1().get_agressive_moves()) != 0:
                                                        if rest[0]:
                                                            game.get_player1().do_active_move(board2, rest[1], rest[2],
                                                                                              vector_move)
                                                            best = max(best,
                                                                       minimax(depth - 1, not is_max_player1, game))
                                                            game = copy.copy(bef_act_game)


                        else:

                            continue
                    else:

                        continue

        return best

    else:

        best = float('inf')

        for board in game.get_player2().get_boards():

            for row in range(ROWS):

                for col in range(COLS):
                    # Check if cell is empty
                    piece = board.get_cell(row, col)
                    save = copy.copy(game)
                    game = copy.copy(save)
                    if piece != 0 and piece.get_color() == game.get_player2().get_color():
                        # calculate and Make the possible passive moves

                        game.get_player2().calc_moves(board, piece)
                        if len(game.get_player2().get_moves()) != 0:

                            # Para cada passive move calculado, efetuar movimento
                            vector_move = []
                            color_played = board.get_color()

                            for move in game.get_player2().get_moves():

                                vector_move = move[0] - piece.get_row(), move[1] - piece.get_col()
                                # movimento passivo efetuado
                                game.get_player2().get_board(board).change_piece_cell(piece, move)

                                # Fazer agressive move

                                for board2 in game.get_boards():

                                    if board2.get_color() != color_played:

                                        for row2 in range(ROWS):

                                            for col2 in range(COLS):
                                                bef_act_game = copy.copy(game)
                                                # Check if cell is empty
                                                piece2 = board2.get_cell(row2, col2)

                                                if piece2 != 0 and piece2.get_color() == game.get_player2().get_color():

                                                    rest = game.get_player2().active_move(board2, vector_move, piece2,
                                                                                          color_played)
                                                    if len(game.get_player2().get_agressive_moves()) != 0:
                                                        if rest[0]:
                                                            game.get_player2().do_active_move(board2, rest[1], rest[2],
                                                                                              vector_move)

                                                            best = max(best,
                                                                       minimax(depth - 1, is_max_player1, game))
                                                            game = copy.copy(bef_act_game)
                                                    # voltar para o estado em que só tinha feito o passive move

                        else:

                            continue
                    else:

                        continue
        return best


def best_move_max_p1(game, depth):
    best = float('-inf')

    best_move_game = None

    for board in game.get_player1().get_boards():

        for row in range(ROWS):

            for col in range(COLS):
                # Check if cell is empty
                piece = board.get_cell(row, col)
                save = copy.copy(game)
                game = copy.copy(save)
                if piece != 0 and piece.get_color() == game.get_player1().get_color():
                    # calculate and Make the possible passive moves

                    game.get_player1().calc_moves(board, piece)
                    if len(game.get_player2().get_moves()) != 0:

                        # Para cada passive move calculado, efetuar movimento
                        vector_move = []
                        color_played = board.get_color()

                        for move in game.get_player1().get_moves():

                            vector_move = move[0] - piece.get_row(), move[1] - piece.get_col()
                            # movimento passivo efetuado
                            game.get_player1().get_board(board).change_piece_cell(piece, move)

                            # Fazer agressive move

                            for board2 in game.get_boards():

                                if board2.get_color() != color_played:

                                    for row2 in range(ROWS):

                                        for col2 in range(COLS):
                                            bef_act_game = copy.copy(game)
                                            # Check if cell is empty
                                            piece2 = board2.get_cell(row2, col2)

                                            if piece2 != 0 and piece2.get_color() == game.get_player1().get_color():

                                                rest = game.get_player1().active_move(board2, vector_move, piece2,
                                                                                      color_played)
                                                if len(game.get_player1().get_agressive_moves()) != 0:
                                                    if rest[0]:
                                                        game.get_player1().do_active_move(board2, rest[1], rest[2],
                                                                                          vector_move)

                                                        move_val = minimax(depth , False, game)

                                                        if move_val > best:
                                                            best = move_val
                                                            best_move_game = copy.copy(game)
                                                            game = copy.copy(bef_act_game)
                                                    # voltar para o estado em que só tinha feito o passive move



                            else:

                                continue
                else:

                    continue

    return best_move_game


def best_move_min_p2(game, depth):
    best = float('inf')
    best_move_game = None
    for board in game.get_player2().get_boards():

        for row in range(ROWS):

            for col in range(COLS):
                # Check if cell is empty
                piece = board.get_cell(row, col)
                save = copy.copy(game)
                game = copy.copy(save)
                if piece != 0 and piece.get_color() == game.get_player2().get_color():
                    # calculate and Make the possible passive moves

                    game.get_player2().calc_moves(board, piece)
                    if len(game.get_player2().get_moves()) != 0:

                        # Para cada passive move calculado, efetuar movimento
                        vector_move = []


                        for move in game.get_player2().get_moves():

                            vector_move = move[0] - piece.get_row(), move[1] - piece.get_col()
                            # movimento passivo efetuado
                            game.get_player2().get_board(board).change_piece_cell(piece, move)
                            color_played = board.get_color()
                            # Fazer agressive move

                            for board2 in game.get_boards():

                                if board2.get_color() != color_played:

                                    for row2 in range(ROWS):

                                        for col2 in range(COLS):
                                            bef_act_game = copy.copy(game)
                                            # Check if cell is empty
                                            piece2 = board2.get_cell(row2, col2)

                                            if piece2 != 0 and piece2.get_color() == game.get_player2().get_color():

                                                rest = game.get_player2().active_move(board2, vector_move, piece2,
                                                                                      color_played)
                                                if len(game.get_player2().get_agressive_moves()) != 0:
                                                    if rest[0]:
                                                        game.get_player2().do_active_move(board2, rest[1], rest[2],
                                                                                          vector_move)

                                                        move_val = minimax(depth , True, game)

                                                        if move_val < best:
                                                            best = move_val
                                                            best_move_game = copy.copy(game)
                                                            game = copy.copy(bef_act_game)
                                                    # voltar para o estado em que só tinha feito o passive move



                            else:

                                continue
                else:

                    continue

    return best_move_game
