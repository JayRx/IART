import pygame
import sys
import shobu
from shobu.Controller.GameController import GameController
from shobu.Model.Board import Board
from shobu.Model.Game import Game
from shobu.Model.Player import Player
from shobu.Model.constants import SQUARE_SIZE, BOARD_OUTLINE, WIDTH, GREEN, BLUE, \
    LIGHT_BROWN, DARK_BROWN, BOARD_PADDING, BLACK, DISPLAY_SIZE, WHITE, MoveDirect
from shobu.View.BoardView import BoardView

from shobu.View.GameView import GameView

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


def passive_mode1(player, color_playing, radius, run, boards, game_view):
    while run:

        result = selected_board_piece(boards)  # obter informações sobre board e peça selecionada

        if result is not None:
            selected_board = result[0]
            selected_x = result[1]
            selected_y = result[2]
            board_x = result[3]
            board_y = result[4]
            row = result[5]
            col = result[6]

            if selected_board is not None:  # Obter peça
                piece = selected_board.get_cell(row, col)  # Obter possível peça ou quadrado vazio

                if piece != 0 and color_playing == piece.get_color():

                    pygame.draw.circle(WIN, BLUE, (selected_x, selected_y), radius)

                    player.calc_moves(selected_board, piece)  # calcular movimentos de peça escolhida
                    moves = player.get_moves()

                    pygame.display.update()
                    aux_row, aux_col = piece.get_cell()

                    # draws the possible moves (w/ green colour) for the selected piece
                    draw_possible_pos(board_x, board_y, moves, radius)

                    vector = None
                    run2 = False
                    while not run2:
                        aux_result = passive_mode2(moves, selected_board, boards, piece, game_view)
                        run2 = aux_result[0]
                        vector = aux_result[1]
                        print("SDadas")

                    game_view.draw_game()
                    pygame.display.update()

                    vector = vector[0] - aux_row, vector[1] - aux_col  # vector do movimento
                    return selected_board.get_color(), vector  # return vector movimento, cor do board onde foi o mov passivo
        else:
            continue


def passive_mode2(moves, board_selected, boards, piece, game_view):
    move_done_pos = []

    for event2 in pygame.event.get():
        if event2.type == pygame.QUIT:  # se clicamos para sair do jogo
            pygame.quit()
            sys.exit()  # se clicamos para sair do jogo

        elif event2.type == pygame.K_SPACE:
            return False, move_done_pos

        if event2.type == pygame.MOUSEBUTTONDOWN:

            pos = pygame.mouse.get_pos()  # obter posição do mouse
            selected_board2 = get_board_hover_mouse(boards, pos)  # Gives the board selected
            if selected_board2.get_index() == board_selected.get_index():
                cell = get_cell_hover_mouse(selected_board2, pos)  # gives the cell we are selecting with the mouse
                row, col = cell
                row = int(row)
                col = int(col)

                passive_move = row, col
                for move in moves:

                    if row == move[0] and col == move[1]:
                        selected_board2.change_piece_cell(piece, passive_move)
                        move_done_pos = row, col
                        game_view.draw_game()
                        return True, move_done_pos

            else:
                continue

    return False, move_done_pos


def selected_board_piece(boards):
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

        else:
            continue


def active_mode2(moves, board_select, boards, piece, game_view,vector_move):
    move_done_pos = []

    for event2 in pygame.event.get():
        if event2.type == pygame.QUIT:  # se clicamos para sair do jogo
            pygame.quit()
            sys.exit()  # se clicamos para sair do jogo

        elif event2.type == pygame.K_SPACE:
            return False, move_done_pos

        if event2.type == pygame.MOUSEBUTTONDOWN:

            pos = pygame.mouse.get_pos()  # obter posição do mouse
            selected_board2 = get_board_hover_mouse(boards, pos)  # Gives the board selected
            if selected_board2 == board_select:
                cell = get_cell_hover_mouse(selected_board2, pos)  # gives the cell we are selecting with the mouse
                row, col = cell
                row = int(row)
                col = int(col)

                active_move = row, col
                for move in moves:

                    if row == move[0] and col == move[1]:

                        #faltam apenas os casos de empurrar duas casas quando peça exatamente à frente da que ataca
                        # deixar de selecionar peças à vontade
                        #vector_move2 = (row - vector_move[0] )//2 ,(col - vector_move[1] )//2

                       #aux_piece2 = piece.get_cell()[0] + vector_move2[0], piece.get_cell()[1] + vector_move2[1]


                        if selected_board2.get_board_info()[row][col] != 0:
                            # verificar se tem peça que pode ser empurrada
                            aux_piece = selected_board2.get_board_info()[row][col]
                            aux_piece2 = aux_piece.get_row() + vector_move[0], aux_piece.get_col() + vector_move[1]
                            result = selected_board2.change_piece_cell(aux_piece, aux_piece2)#empurramos peça, mudando de célula

                            if result is not True:  # se peça a ser empurrada, não alocada no tabuleiro, é porque foi empurrada para fora

                                #selected_board2.get_board_info()[row][col] = 0  # eliminiamos peça
                                selected_board2.change_piece_cell(piece, active_move)  # movemos a peça que empurrou
                            else:
                                selected_board2.change_piece_cell(piece, active_move) #mover peça para o espaço vazio de onde estava peça que foi empurrada mas não eliminada
                        else:
                            selected_board2.change_piece_cell(piece, active_move)


                        move_done_pos = row, col
                        game_view.draw_game()
                        return True, move_done_pos

            else:
                continue

    return False, move_done_pos


def active_mode1(run, color_board_played, color_playing, player, radius, boards, game_view, vector_move):
    while run:

        result = selected_board_piece(boards)  # obter informações sobre board e peça selecionada

        if result is not None:
            selected_board = result[0]
            selected_x = result[1]
            selected_y = result[2]
            board_x = result[3]
            board_y = result[4]
            row = result[5]
            col = result[6]

            if selected_board is not None:  # Obter peça
                piece = selected_board.get_cell(row, col)  # Obter possível peça ou quadrado vazio

                if piece != 0 and color_playing == piece.get_color() and color_board_played != selected_board.get_color():

                    pygame.draw.circle(WIN, BLUE, (selected_x, selected_y), radius)

                    player.agr_move_cal(selected_board, vector_move, piece)  # calcular movimentos de peça escolhida
                    moves = player.get_agressive_moves()

                    pygame.display.update()
                    aux_row, aux_col = piece.get_cell()

                    draw_possible_pos(board_x, board_y, moves, radius - 10)

                    vector = None
                    run2 = False
                    while not run2:
                        aux_result = active_mode2(moves, selected_board, boards, piece, game_view,vector_move)
                        run2 = aux_result[0]
                        vector = aux_result[1]
                        print("active mode")

                    game_view.draw_game()
                    pygame.display.update()

                    vector = vector[0] - aux_row, vector[1] - aux_col  # vector do movimento
                    return vector, selected_board.get_color()  # return vector movimento, cor do board onde foi o mov passivo
            else:
                continue


def draw_possible_pos(board_x, board_y, moves, radius):
    for move in moves:
        row, col = move
        # Transformações dos valores para desenhar tendo em conta tada a janela do jogo
        move_x = board_x + (SQUARE_SIZE + BOARD_OUTLINE) * col + SQUARE_SIZE // 2
        move_y = board_y + (SQUARE_SIZE + BOARD_OUTLINE) * row + SQUARE_SIZE // 2
        pygame.draw.circle(WIN, GREEN, (move_x, move_y), radius)
        # refresh display

    pygame.display.update()


def evaluate_move(last_pos, new_pos):
    info_move = []
    if new_pos[0] == last_pos[0] and new_pos[1] > last_pos:
        info_move.append(MoveDirect.right)


def main():
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

    player1 = Player(BLACK)
    player2 = Player(WHITE)

    game = Game(boards, player1, player2)

    game_view = GameView(game, WIN)
    board_view = BoardView()

    game_controller = GameController(game, game_view)

    while run:
        game_controller.start()
        # pygame.draw.circle(WIN, GREEN, (383.0, 435.0), radius)
        pygame.display.update()
        aux_boards = game.get_boards()
        result = passive_mode1(player1, player1.get_color(), radius, run, aux_boards, game_view)
        print("out")

        game_view = GameView(game, WIN)
        game_view.draw_game()
        pygame.display.update()

        """piece = aux_boards[2].get_board_info()[3][2]
        player1.agr_move_cal(aux_boards[2], result[0], piece)
        aux_list = player1.get_agressive_moves()
        """

        active_mode1(run, result[0], player1.get_color(), player1, radius, aux_boards, game_view, result[1])

        print("hey")

        """for move in aux_list:
            row, col = move
            board_x, board_y = aux_boards[2].get_pos()
            # Transformações dos valores para desenhar tendo em conta tada a janela do jogo
            move_x = board_x + (SQUARE_SIZE + BOARD_OUTLINE) * col + SQUARE_SIZE // 2
            move_y = board_y + (SQUARE_SIZE + BOARD_OUTLINE) * row + SQUARE_SIZE // 2
            pygame.draw.circle(WIN, GREEN, (move_x, move_y), radius)
            # refresh display"""

        pygame.display.update()
        result = passive_mode1(player2, player2.get_color(), radius, run, aux_boards, game_view)

        active_mode1(run, result[0], player2.get_color(), player2, radius, aux_boards, game_view, result[1])

        print(run)
    # passive_mode1(player2, player2.get_color(), radius, run, game.get_boards(), game_view)


"""
    # Continuar jogo
    run = True
    while run:
        game_view.drawGame(WIN, board_view, game)

        pygame.display.update()"""

main()
