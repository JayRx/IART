import math

import pygame
import sys
import shobu
from shobu.Controller.GameController import GameController
from shobu.Model.Board import Board
from shobu.Model.Game import Game
from shobu.Model.Player import Player
from shobu.Model.constants import SQUARE_SIZE, BOARD_OUTLINE, WIDTH, GREEN, BLUE, \
    LIGHT_BROWN, DARK_BROWN, BOARD_PADDING, BLACK, DISPLAY_SIZE, WHITE, MoveDirect, ROWS, COLS
from shobu.View.BoardView import BoardView

from shobu.View.GameView import GameView

from shobu.Heuristics.Heuristics import *
from shobu.View.PlayerView import PlayerView

FPS = 60

WIN = pygame.display.set_mode((DISPLAY_SIZE, DISPLAY_SIZE))  # Display game

pygame.display.set_caption('Shobu')


def get_board_hover_mouse(boards, pos):
    x, y = pos

    for board in boards:
        board_x, board_y = board.get_pos()
        if board_x <= x <= board_x + board.get_size():
            if board_y <= y <= board_y + board.get_size():
                return board
    return None


def get_cell_hover_mouse(board, pos):
    x, y = pos
    board_x, board_y = board.get_pos()
    row = (y - board_y) // (SQUARE_SIZE + BOARD_OUTLINE)
    col = (x - board_x) // (SQUARE_SIZE + BOARD_OUTLINE)

    return row, col  # returna posição da célula


def passive_mode1(player, color_playing, selected_board_info_piece):
    result = selected_board_info_piece  # obter informações sobre board e peça selecionada
    player.restart_passive_moves()
    if result is not None:
        selected_board = result[0]
        row = result[5]
        col = result[6]

        if selected_board is not None:  # Obter peça
            piece = selected_board.get_cell(row, col)  # Obter possível peça ou quadrado vazio

            index = -1

            for board in player.get_boards():
                if board.get_index() == selected_board.get_index():
                    index = selected_board.get_index()

            if piece != 0 and color_playing == piece.get_color() and index != -1:  # temos de ter selecionado uma peça e ser um tabuleiro que pertence ao player

                player.calc_moves(selected_board, piece)  # calcular movimentos de peça escolhida

                return True

        else:
            return False


    else:
        return False


def passive_mode2(moves, board_selected, piece, selected_board_info_piece, move_done_pos):
    result = selected_board_info_piece

    if result is not None:
        selected_board2 = result[0]
        row = result[5]
        col = result[6]

        if selected_board2.get_index() == board_selected.get_index():  # se vamos tentar efetuar passive_move no board correto

            passive_move = row, col
            for move in moves:
                # verifica se o que selecionamos é um espaço dentro dos passive_moves possíveis
                if row == move[0] and col == move[1]:
                    selected_board2.change_piece_cell(piece, passive_move)

                    move_done_pos.append(row)
                    move_done_pos.append(col)

                    return True  # Peça é movida há posição para a qual já movemos a peça

        else:
            move_done_pos.append(row)
            move_done_pos.append(col)

            return False  # peça não é movida, logo não há movimento efetuado no board
    else:
        move_done_pos = None  # não selecionei qualquer board ou peça
        return False


def selected_board_piece(boards):
    FPS = 60
    clock = pygame.time.Clock()
    clock.tick(FPS)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  # se clicamos para sair do jogo

        elif event.type == pygame.MOUSEBUTTONDOWN:  # Se clicarmos em algo

            pos = pygame.mouse.get_pos()  # obter posição do mouse
            selected_board = get_board_hover_mouse(boards, pos)  # Gives the board selected

            cell = get_cell_hover_mouse(selected_board, pos)  # gives the cell we are selecting with the mouse
            row, col = cell
            row = int(row)
            col = int(col)

            board_x, board_y = selected_board.get_pos()  # gives the position of the board we are selecting with the mouse
            selected_x = board_x + (SQUARE_SIZE + BOARD_OUTLINE) * col + SQUARE_SIZE // 2
            selected_y = board_y + (SQUARE_SIZE + BOARD_OUTLINE) * row + SQUARE_SIZE // 2

            return selected_board, selected_x, selected_y, board_x, board_y, row, col

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return -1

        else:
            continue

    return None


def get_mouse_pos():
    pos = None
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  # se clicamos para sair do jogo


        elif event.type == pygame.MOUSEBUTTONDOWN:  # Se clicarmos em algo

            pos = pygame.mouse.get_pos()

        else:
            continue

    return pos


def active_mode2(moves, board_selected, piece, selected_board_info_piece, vector_move):
    result = selected_board_info_piece

    if result is not None:
        selected_board2 = result[0]
        row = result[5]
        col = result[6]

        if selected_board2.get_index() == board_selected.get_index():  # verify if the board selected is the same we have in the parameter board_selected

            active_move = row, col
            for move in moves:

                if row == move[0] and col == move[1]:
                    previous_cell = piece.get_row(), piece.get_col()

                    if selected_board2.get_board_info()[row][
                        col] != 0:  # tem uma peça para onde pretendo fazer uma active_move

                        # verificar se tem peça que pode ser empurrada
                        aux_piece = selected_board2.get_board_info()[row][col]
                        aux_cell_dest = aux_piece.get_row() + vector_move[0] // 2, aux_piece.get_col() + \
                                        vector_move[1] // 2

                        result = selected_board2.change_piece_cell(aux_piece,
                                                                   aux_cell_dest)  # Tentamos empurrar peça, mudando de célula

                        if result is not True:  # se peça a ser empurrada, não alocada no tabuleiro, é porque foi empurrada para fora/change_piece retorna False

                            selected_board2.change_piece_cell(piece,
                                                              active_move)  # movemos a peça que empurrou, peça que sai do tabuleiro também é eliminada

                        else:  # se peça a ser empurrada fica dentro do tabuleiro e foi empurrada
                            selected_board2.change_piece_cell(piece,
                                                              active_move)  # mover peça para o espaço vazio de onde estava peça que foi empurrada mas não eliminada

                    else:  # se movimento é para um espaço vazio e está dentro dos active_moves possíveis
                        selected_board2.change_piece_cell(piece, active_move)

                        # caso em que se avança duas casas e temos uma peça adversária no caminho e tem de ser
                        # empurrada

                    if abs(vector_move[0]) > 1 or abs(
                            vector_move[1]) > 1:  # evitar empurrar peças que estão uma
                        # seguir À outra
                        aux_move = previous_cell[0] + vector_move[0] // 2, previous_cell[1] + vector_move[
                            1] // 2  # obter possível peça uma casa antes do mov de duas casas
                        poss_piece = selected_board2.get_board_info()[aux_move[0]][aux_move[1]]

                        # certificar que que casos em que se empurra uma peça, não tem outras peças a impedir ,
                        # várias configurações possíveis
                        if selected_board2.get_board_info()[aux_move[0]][
                            aux_move[1]] != 0 and piece.get_color() != poss_piece.get_color() and \
                                selected_board2.get_board_info()[previous_cell[0]][previous_cell[1]] == 0:
                            cell_dest = poss_piece.get_row() + vector_move[0], poss_piece.get_col() + vector_move[1]

                            selected_board2.change_piece_cell(poss_piece, cell_dest)

                    return True
        else:
            return False

    else:
        return False


def active_mode1(player, color_board_played, vector_move,
                 selected_board_info_piece):
    # obter informações sobre board e peça selecionada
    player.restart_active_moves()
    result = selected_board_info_piece
    if result is not None and result != - 1:

        selected_board = result[0]

        row = result[5]
        col = result[6]

        if selected_board is not None:  # Obter peça
            piece = selected_board.get_cell(row, col)  # Obter possível peça ou quadrado vazio

            if piece != 0 and player.get_color() == piece.get_color() and color_board_played != selected_board.get_color():

                player.agr_move_cal(selected_board, vector_move, piece)  # calcular movimentos de peça escolhida
                moves = player.get_agressive_moves()
                aux_row, aux_col = piece.get_cell()

                # verificar moves tendo em conta o vector move do passive_move e mais algumas restrições
                if abs(vector_move[0]) > 1 or abs(vector_move[1]) > 1:  # evitar empurrar peças que estão uma
                    # seguir À outra (quando se anda duas casas)
                    aux_move = aux_row + vector_move[0] // 2, aux_col + vector_move[1] // 2
                    if ROWS - 1 >= aux_move[0] >= 0 and aux_move[1] <= COLS - 1 and aux_move[
                        1] >= 0:

                        if ROWS - 1 >= moves[0][0] >= 0 and moves[0][1] <= COLS - 1 and moves[0][
                            1] >= 0:

                            if selected_board.get_board_info()[aux_move[0]][aux_move[1]] != 0 and piece.get_color() == \
                                    selected_board.get_board_info()[aux_move[0]][aux_move[1]].get_color():
                                player.set_active_moves([])
                                return False

                            # Casos mov duas casas, onde empurrar uma peça pode não ser possível, por ter peças atrás: Juntas, intervaladas ambas as cores
                            elif selected_board.get_board_info()[aux_move[0]][aux_move[1]] != 0 and \
                                     selected_board.get_board_info()[moves[0][0]][moves[0][
                                        1]] != 0:  # and  selected_board.get_board_info()[moves[0][0] + aux_move[0]][moves[0][1] + aux_move[1]] != 0:
                                player.set_active_moves([])
                                return False

                else:  # caso de empurrar (deslocando uma casa) mas está uma peça a seguir a impedir (ex: xoo, x,
                    # o peças, empurra para a direita)
                    aux_move = aux_row + vector_move[0] * 2, aux_col + vector_move[1] * 2
                    aux_move2 = aux_row + vector_move[0], aux_row + vector_move[1]

                    if ROWS - 1 >= aux_move[0] >= 0 and aux_move[1] <= COLS - 1 and aux_move[
                        1] >= 0:
                        if ROWS - 1 >= aux_move2[0] >= 0 and aux_move2[1] <= COLS - 1 and aux_move2[
                            1] >= 0:

                            if selected_board.get_board_info()[aux_move[0]][aux_move[1]] != 0 and \
                                    selected_board.get_board_info()[aux_move2[0]][
                                        aux_move2[1]] != 0 and piece.get_color() != \
                                    selected_board.get_board_info()[aux_move[0]][aux_move[1]].get_color():
                                player.set_active_moves([])
                                return False

        return True

    else:
        return False


def main():
    FPS = 30

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

    heuristics = Heuristics()

    game_controller.start()
    while run:

        game_view = GameView(WIN)
        player_play(game, game_view, player1,
                    player1_view)

        player_play(game, game_view, player2, player2_view)

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
    else:
        empty_result = []
        return empty_result

        res = game_controller.objective_test(aux_boards, player1)
        if res == -1:
            print("game isn't over!")

        heuristics.calc(aux_boards, player1)
        heuristics.print_value()

        """for move in aux_list:
            row, col = move
            board_x, board_y = aux_boards[2].get_pos()
            # Transformações dos valores para desenhar tendo em conta tada a janela do jogo
            move_x = board_x + (SQUARE_SIZE + BOARD_OUTLINE) * col + SQUARE_SIZE // 2
            move_y = board_y + (SQUARE_SIZE + BOARD_OUTLINE) * row + SQUARE_SIZE // 2
            pygame.draw.circle(WIN, GREEN, (move_x, move_y), radius)
            # refresh display"""
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


def player_play(game, game_view, player, player_view,
                ):
    # Variáveis necessárias para jogada iterativa

    boards = game.get_boards()
    selected_board_info_piece = None
    vector_for_active = None
    color_board_passive_move = None
    phase1_player = False

    while not phase1_player:
        move_done_pos = []
        game_view.draw_game(game)
        result = False
        while not result:

            selected_board_info_piece = selected_board_piece(boards)
            if selected_board_info_piece is not None:
                result = passive_mode1(player, player.get_color(), selected_board_info_piece)

        selected_x = selected_board_info_piece[1]
        selected_y = selected_board_info_piece[2]
        board_x = selected_board_info_piece[3]
        board_y = selected_board_info_piece[4]
        row = selected_board_info_piece[5]
        col = selected_board_info_piece[6]
        # Para cálculo do vetor do movimento final selecionado

        piece_selected = selected_board_info_piece[0].get_cell(row, col)
        aux_row, aux_col = piece_selected.get_cell()

        # sinalizar que peça selecionei
        player_view.draw_view_piece_select(selected_x, selected_y, BLUE)
        game_view.refresh_window()
        # draws the possible moves (w/ green colour) for the selected piece
        #  draw_possible_pos(board_x, board_y, moves, radius)

        player_view.draw_passive_moves(board_x, board_y, player)

        game_view.refresh_window()

        # verificar se prefiro selecionar outra peça
        result = False
        while not result:

            selected_board_info_piece = selected_board_piece(boards)

            if selected_board_info_piece == -1:
                result = True

            elif selected_board_info_piece is not None:
                result = passive_mode2(player.get_moves(), selected_board_info_piece[0], piece_selected,
                                       selected_board_info_piece,
                                       move_done_pos)
                if result is True:  # já selecionamos um movimento possível
                    color_board_passive_move = selected_board_info_piece[0].get_color()
                    # vetor para movimento para o active_mode

                    vector_for_active = move_done_pos[0] - aux_row, move_done_pos[
                        1] - aux_col  # vector do movimento
                    color_board_passive_move = selected_board_info_piece[
                        0].get_color()  # Obter cor do board onde se fez uma jogada completa
                    phase1_player = True  # passive mode termina
        # refresh do ecrã com nova configuração do jogo

        game_view.draw_game(game)
    # active phase
    phase2_player = False
    # Phase2
    while not phase2_player:
        game_view.draw_game(game)
        result = False

        while not result:

            selected_board_info_piece = selected_board_piece(boards)
            if selected_board_info_piece is not None:
                result = active_mode1(player, color_board_passive_move, vector_for_active,
                                      selected_board_info_piece)

        # informaações sobre o local, pe
        selected_x = selected_board_info_piece[1]
        selected_y = selected_board_info_piece[2]
        board_x = selected_board_info_piece[3]
        board_y = selected_board_info_piece[4]
        row = selected_board_info_piece[5]
        col = selected_board_info_piece[6]

        # sinalizar que peça selecionei
        piece_selected = selected_board_info_piece[0].get_cell(row, col)

        player_view.draw_view_piece_select(selected_x, selected_y, RED)

        # draws the possible moves (w/ green colour) for the selected piece
        #  draw_possible_pos(board_x, board_y, moves, radius)

        player_view.draw_active_moves(board_x, board_y, player)

        game_view.refresh_window()
        selected_board = selected_board_info_piece[0]

        # phase2
        
        selected_board_info_piece = None
        result = False
        while not result:

            selected_board_info_piece = selected_board_piece(boards)

            if selected_board_info_piece == -1:
                result = True  # voltar a selecionar outra peça

            elif selected_board_info_piece is not None:
                result = active_mode2(player.get_agressive_moves(), selected_board, piece_selected,
                                      selected_board_info_piece, vector_for_active)

                if result is True:
                    phase2_player = True

            else:
                continue
    game_view.draw_game(game)

    return True


"""
    # Continuar jogo
    run = True
    while run:
        game_view.drawGame(WIN, board_view, game)

        pygame.display.update()"""

main()
