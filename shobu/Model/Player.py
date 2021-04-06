import sys

import pygame

from shobu.Heuristics.Heuristics import Heuristics
from shobu.Model.constants import ROWS, COLS, SQUARE_SIZE, BOARD_OUTLINE, RED, BLUE
from shobu.Model.Board import Board


class Player:

    def __init__(self, color, boards):
        self.__win_state = False
        self.__color = color
        self.__moves = []
        self.__aggressive_moves = []
        self.__row = 0
        self.__col = 0
        self.__boards = boards

    def get_state(self):
        return self.__win_state

    def calc_moves2(self, board, piece):
        self.restart_passive_moves()

        self.__row = piece.get_row()
        self.__col = piece.get_col()
        for i in range(2):
            # LEFT
            if self.__row > i:
                self.__moves.append([self.__row - 1 - i, self.__col])

            # RIGHT
            if self.__row < ROWS - 1 - i:
                self.__moves.append([self.__row + 1 + i, self.__col])

            # DOWN
            if self.__col > i:
                self.__moves.append([self.__row, self.__col - 1 - i])

            # UP
            if self.__col < COLS - 1 - i:
                self.__moves.append([self.__row, self.__col + 1 + i])

            # LEFT DOWN
            if self.__row > i and self.__col > i:
                self.__moves.append([self.__row - 1 - i, self.__col - 1 - i])

            # RIGHT DOWN
            if self.__row < ROWS - 1 - i and self.__col > i:
                self.__moves.append([self.__row + 1 + i, self.__col - 1 - i])

            # LEFT UP
            if self.__row > i and self.__col < COLS - 1 - i:
                self.__moves.append([self.__row - 1 - i, self.__col + 1 + i])

            # RIGHT UP
            if self.__row < ROWS - 1 - i and self.__col < COLS - 1 - i:
                self.__moves.append([self.__row + 1 + i, self.__col + 1 + i])

        aux_moves = self.__moves.copy()  # evita algum valor ser ignorado , quando removemos vários elementos
        for move in self.__moves:
            # imp_moves = []
            move_row, move_col = move
            cell = board.get_cell(move_row, move_col)
            if cell != 0 and self.get_color() != cell.get_color():
                continue

            elif cell != 0 and self.get_color() == cell.get_color():

                aux_moves.remove(move)
        self.__moves = aux_moves
        # Verificar movimentos impossíveis por terem uma peça antes à frente
        return self.__moves

    def calc_moves(self, board, piece):
        self.restart_passive_moves()
        self.__moves = []
        i_list = [-1, 0, 1]
        j_list = [-1, 0, 1]
        self.__row = piece.get_row()
        self.__col = piece.get_col()

        if piece != 0 and piece.get_color() == self.get_color():
            for i2 in i_list:
                for j2 in j_list:
                    if 0 <= self.__row + i2 < ROWS and 0 <= self.__col + j2 < COLS and board.get_cell(self.__row + i2,
                                                                                                      self.__col + j2) == 0:
                        self.__moves.append([self.__row + i2, self.__col + j2])

            for i2 in i_list:
                for j2 in j_list:
                    if 0 <= self.__row + i2 * 2 < ROWS and 0 <= self.__col + j2 * 2 < COLS and board.get_cell(
                            self.__row + i2 * 2, self.__col + j2 * 2) == 0 and board.get_cell(self.__row + i2,
                                                                                              self.__col + j2) == 0:
                        self.__moves.append([self.__row + i2 * 2, self.__col + j2 * 2])

        return self.__moves

    def set_selected_piece_pos(self, piece):
        self.__row = piece.get_row()
        self.__col = piece.get_col()

    def active_move(self, board_to_play, vector_move, piece_to_move, color_board_played):
        self.get_agressive_moves().clear()
        if board_to_play.get_color() != color_board_played:

            # Casos de movimento , deslocamento de duas células
            if abs(vector_move[0]) > 1 or abs(vector_move[1]) > 1:
                # casos de vetor do movimento de duas casas:
                aux_vect = vector_move[0] // 2, vector_move[1] // 2
                # Três possíveis células a seguir à peça a mover
                cell1 = piece_to_move.get_row() + aux_vect[0], piece_to_move.get_col() + aux_vect[1]
                cell2 = piece_to_move.get_row() + vector_move[0], piece_to_move.get_col() + vector_move[1]
                cell3 = piece_to_move.get_row() + aux_vect[0] * 3, piece_to_move.get_col() + aux_vect[1] * 3

                # Caso XO__

                if self.verify_limits(cell1) and self.verify_limits(cell2) and self.verify_limits(cell3):
                    if self.verify_is_piece_dif_color(cell1, board_to_play) and not self.verify_is_piece(
                            cell2, board_to_play) and not self.verify_is_piece(cell3, board_to_play):
                        new_local = cell2
                        self.__aggressive_moves.append(new_local)
                        return True, piece_to_move, cell1, vector_move

                # Caso XO_$, where $ is out of the board
                if self.verify_limits(cell1) and self.verify_limits(cell2) and not self.verify_limits(cell3):
                    if self.verify_is_piece_dif_color(cell1, board_to_play) and not self.verify_is_piece(cell2,
                                                                                                         board_to_play):
                        new_local = cell2
                        self.__aggressive_moves.append(new_local)
                        return True, piece_to_move, cell1, vector_move
                # Caso X_O$
                if self.verify_limits(cell1) and self.verify_limits(cell2) and not self.verify_limits(cell3):
                    if not self.verify_is_piece(cell1, board_to_play) and self.verify_is_piece_dif_color(cell2,
                                                                                                         board_to_play):
                        new_local = cell2
                        self.__aggressive_moves.append(new_local)
                        return True, piece_to_move, cell2, vector_move

                # Caso X_O_
                if self.verify_limits(cell1) and self.verify_limits(cell2) and self.verify_limits(cell3):
                    if not self.verify_is_piece(cell1, board_to_play) and self.verify_is_piece_dif_color(
                            cell2, board_to_play) and not self.verify_is_piece(cell3, board_to_play):
                        new_local = cell2
                        self.__aggressive_moves.append(new_local)

                        return True, piece_to_move, cell2, vector_move

                # Caso X__
                if self.verify_limits(cell1) and self.verify_limits(cell2):
                    if not self.verify_is_piece(cell1, board_to_play) and not self.verify_is_piece(cell2,
                                                                                                   board_to_play):
                        new_local = cell2
                        self.__aggressive_moves.append(new_local)
                        return True, piece_to_move, [], vector_move  # [] indica que não há peça do adversário a
                        # deslocar


            else:
                cell1 = piece_to_move.get_row() + vector_move[0], piece_to_move.get_col() + vector_move[1]
                cell2 = piece_to_move.get_row() + vector_move[0] * 2, piece_to_move.get_col() + vector_move[1] * 2
                # caso XO_
                if self.verify_limits(cell1) and self.verify_limits(cell2):
                    if self.verify_is_piece_dif_color(cell1, board_to_play) and not self.verify_is_piece(cell2,
                                                                                                         board_to_play):
                        new_local = cell1
                        self.__aggressive_moves.append(cell1)
                        return True, piece_to_move, cell1, vector_move

                # Caso XO$
                if self.verify_limits(cell1) and not self.verify_limits(cell2):
                    if self.verify_is_piece_dif_color(cell1, board_to_play):
                        new_local = cell1
                        self.__aggressive_moves.append(new_local)

                        return True, piece_to_move, cell1, vector_move
                # Caso X_(_ ou $)
                if self.verify_limits(cell1):
                    if not self.verify_is_piece(cell1, board_to_play):
                        new_local = cell1
                        self.__aggressive_moves.append(new_local)
                        return True, piece_to_move, [], vector_move

        return False, [], [], []

    def do_active_move(self, board, piece_to_move, adv_piece, vector_move):
        if len(adv_piece) != 0:

            aux_vec = vector_move[0] // 2, vector_move[1] // 2
            cell1 = adv_piece[0] + aux_vec[0], adv_piece[1] + aux_vec[1]
            cell2 = adv_piece[0] + aux_vec[0], adv_piece[1] - aux_vec[1]

            if abs(vector_move[0]) > 1 or abs(vector_move[1]) < 1 and self.verify_limits(cell1) and self.verify_limits(
                    cell2) and not self.verify_is_piece(cell1, board) and not self.verify_is_piece(cell2, board):

                new_row = adv_piece[0] + aux_vec[0]
                new_col = adv_piece[1] + aux_vec[1]
                piece = board.get_cell(adv_piece[0], adv_piece[1])
                board.change_piece_cell(piece, (new_row, new_col))
            else:

                new_row = adv_piece[0] + vector_move[0]
                new_col = adv_piece[1] + vector_move[1]
                piece = board.get_cell(adv_piece[0], adv_piece[1])
                board.change_piece_cell(piece, (new_row, new_col))

        new_row = piece_to_move.get_row() + vector_move[0]
        new_col = piece_to_move.get_col() + vector_move[1]
        board.change_piece_cell(piece_to_move, (new_row, new_col))

    def verify_limits(self, cell):
        if cell[0] > ROWS - 1 or cell[0] < 0 or cell[1] > COLS - 1 or cell[1] < 0:
            return False
        else:
            return True

    def verify_is_piece_dif_color(self, cell, board):

        if self.verify_limits(cell):
            if board.get_cell2(cell) != 0 and board.get_cell2(cell).get_color() != self.get_color():

                return True
            else:
                return False

        else:
            return False

    def verify_is_piece(self, cell, board):

        if self.verify_limits(cell):
            if board.get_cell2(cell) != 0:

                return True
            else:
                return False

        else:
            return False

    def verify_is_piece_equal_color(self, cell, board):

        if self.verify_limits(cell):
            if board.get_cell2(cell) != 0 and board.get_cell2(cell).get_color() == self.get_color():

                return True
            else:
                return False

        else:
            return False

    def get_color(self):
        return self.__color

    def get_moves(self):
        return self.__moves

    def get_agressive_moves(self):
        return self.__aggressive_moves

    def restart_passive_moves(self):
        self.__moves = []

    def restart_active_moves(self):
        self.__aggressive_moves = []

    def get_boards(self):
        return self.__boards

    def get_board(self,board):
        for x in self.get_boards():
            if x.get_index() == board.get_index():
                return x

    def set_active_moves(self, active_moves):
        self.__aggressive_moves = active_moves


def player_play(game, game_view, player, player_view,
                ):
    # Variáveis necessárias para jogada iterativa

    boards = game.get_boards()
    selected_board_info_piece = None
    vector_for_active = None
    color_board_passive_move = None
    phase1_player = False

    heuristics = Heuristics()

    heuristics.calc(boards, player)
    heuristics.print_value()

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
        piece = None
        board = None
        aux_result = None
        while not result:

            selected_board_info_piece = selected_board_piece(boards)

            if selected_board_info_piece is not None and selected_board_info_piece[
                0].get_color() != color_board_passive_move:
                board = selected_board_info_piece[0]
                row = selected_board_info_piece[5]
                col = selected_board_info_piece[6]

                if player.verify_limits((row, col)) and player.verify_is_piece_equal_color((row, col), board):
                    piece = board.get_cell(row, col)
                    aux_result = player.active_move(board, vector_for_active, piece, color_board_passive_move)
                    if aux_result[0] is True:
                        result = True

        # Sinalizar peça que pretendo usar no active_mode
        selected_x = selected_board_info_piece[1]
        selected_y = selected_board_info_piece[2]
        # Desenhar movimentos activos possíveis
        if len(player.get_agressive_moves()) != 0:
            player_view.draw_view_piece_select(selected_x, selected_y, RED)

            board_x = selected_board_info_piece[3]
            board_y = selected_board_info_piece[4]
            print(player.get_agressive_moves())
            player_view.draw_active_moves(board_x, board_y, player)

        result = False
        while not result:
            selected_board_info_piece = selected_board_piece(boards)
            if selected_board_info_piece == -1:  # Pretendo selecionar outra peça
                result = True
            else:

                if selected_board_info_piece is not None and selected_board_info_piece[
                    0].get_color() != color_board_passive_move and len(player.get_agressive_moves()) != 0:

                    board2 = selected_board_info_piece[0]
                    row = selected_board_info_piece[5]  # Local onde escolhi jogar
                    col = selected_board_info_piece[6]

                    act_move = player.get_agressive_moves()[0]
                    act_move_row, act_move_col = act_move[0], act_move[1]

                    if player.verify_limits((row, col)) and board2.get_index() == board.get_index():

                        if act_move_row == row and act_move_col == col:  # movimento activo possível foi o que selecionei
                            player.do_active_move(board2, piece, aux_result[2], vector_for_active)
                            result = True
                            phase2_player = True
                        else:
                            continue

        game_view.draw_game(game)


def get_board_hover_mouse(boards, pos):
    x, y = pos

    for board in boards:
        board_x, board_y = board.get_pos()
        if board_x <= x <= board_x + board.get_size():
            if board_y <= y <= board_y + board.get_size():
                return board
    return None


def get_cell_hover_mouse(board, pos):
    if board == None:
        return None, None
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
            if row == None or col == None:
                return None
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



def obtain_opposite_color_boards(self, color_board_played):
    board_index_diff_color = []
    for board in self.__game.get_boards():
        if board.get_color() != color_board_played:
            board_index_diff_color.append(board.get_index())
    return board_index_diff_color
