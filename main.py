import pygame

import shobu
from shobu.Model.Board import Board
from shobu.Model.Game import Game
from shobu.Model.Player import Player
from shobu.Model.constants import SQUARE_SIZE, BOARD_OUTLINE, WIDTH, GREEN, BLUE, \
    LIGHT_BROWN, DARK_BROWN, BOARD_PADDING, BLACK, DISPLAY_SIZE, WHITE
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


def Passive_mode(color_playing, radius, run, boards, passive_move, previous_cell):
    global piece
    while run:

        # Control variables for two fases of passive_mode
        first_passive_move = False
        passive_move_done = False

        moves = list
        passive_move = None
        for event in pygame.event.get():
            selected_board = None
            selected_board2 = None
            if event.type == pygame.QUIT:  # se clicamos para sair do jogo
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN and not first_passive_move and not passive_move_done:  # Se clicarmos em algo
                pos = pygame.mouse.get_pos()  # obter posição do mouse
                selected_board = get_board_hover_mouse(boards, pos)  # Gives the board selected

                cell = get_cell_hover_mouse(selected_board, pos)  # gives the cell we are selecting with the mouse
                row, col = cell
                row = int(row)
                col = int(col)

                board_x, board_y = selected_board.get_pos()  # gives the position of the board we are selecting with the mouse
                selected_x = board_x + (SQUARE_SIZE + BOARD_OUTLINE) * col + SQUARE_SIZE // 2
                selected_y = board_y + (SQUARE_SIZE + BOARD_OUTLINE) * row + SQUARE_SIZE // 2

                if selected_board != None:  # Obter peça
                    piece = selected_board.get_cell(row, col)  # Obter possível peça ou quadrado vazio

                    if piece != 0 and color_playing == piece.get_color():
                        first_passive_move = True
                        pygame.draw.circle(WIN, BLUE, (selected_x, selected_y), radius)
                        moves = piece.get_moves()
                        previous_cell = piece.get_cell()  # guarda posição de pedra antes de a mover

                        # draws the possible moves (w/ green colour) for the selected piece
                        for move in moves:
                            row, col = move
                            # Transformações dos valores para desenhar tendo em conta tada a janela do jogo
                            move_x = board_x + (SQUARE_SIZE + BOARD_OUTLINE) * col + SQUARE_SIZE // 2
                            move_y = board_y + (SQUARE_SIZE + BOARD_OUTLINE) * row + SQUARE_SIZE // 2
                            pygame.draw.circle(WIN, GREEN, (move_x, move_y), radius)
                        # refresh display
                        pygame.display.update()

            else:
                continue
            # verificar o que selecionamos após selecionar uma peça preta
            while (first_passive_move and not passive_move_done):

                for event2 in pygame.event.get():
                    if event2.type == pygame.QUIT:  # se clicamos para sair do jogo
                        run = False
                        first_passive_move = False

                    if event2.type == pygame.MOUSEBUTTONDOWN and first_passive_move and not passive_move_done:  # Se clicarmos em algo

                        pos = pygame.mouse.get_pos()  # obter posição do mouse
                        selected_board2 = get_board_hover_mouse(boards, pos)  # Gives the board selected
                        if selected_board2.index == selected_board.index:
                            cell = get_cell_hover_mouse(selected_board2,
                                                        pos)  # gives the cell we are selecting with the mouse
                            row, col = cell
                            row = int(row)
                            col = int(col)
                        else:
                            first_passive_move = False
                            selected_board2.draw(WIN)
                            pygame.display.update()

                        passive_move = row, col

                        for move in moves:

                            if row == move[0] and col == move[1]:
                                selected_board2.change_piece_cell(piece, passive_move)
                                passive_move_done = True

                                # Desenhar board actualizado e pronto para o modo agressivo
                                selected_board2.draw(WIN)
                                break

                        if passive_move_done:
                            selected_board2.draw(WIN)
                            pygame.display.update()
                            run = False

                            break
                        else:
                            first_passive_move = False
                            selected_board2.draw(WIN)


def main():
    radius = SQUARE_SIZE // 2 - 10

    run = True
    clock = pygame.time.Clock()

    boards = [Board(0, 0, DARK_BROWN, 0), Board(0, 1, LIGHT_BROWN, 1), Board(1, 0, DARK_BROWN, 2),
              Board(1, 1, LIGHT_BROWN, 3)]
    # Passive move

    player1 = Player(BLACK)
    player2 = Player(WHITE)
    game = Game(boards, player1, player2)
    clock.tick(FPS)
    game_view = GameView(game, WIN)
    board_view = BoardView()

    clock.tick(FPS)

    while run:
        game_view.drawGame(WIN, board_view, game)

        pygame.display.update()

        color_playing = BLACK
        passive_move = None
        previous_cell = None

        Passive_mode(color_playing, radius, run, boards, passive_move, previous_cell)

    # Continuar jogo
    run = True
    while run:
        game_view.drawGame(WIN, board_view, game)

        pygame.display.update()


main()
