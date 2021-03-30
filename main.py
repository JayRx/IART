import pygame
import sys
import shobu
from shobu.Controller.GameController import GameController
from shobu.Model.Board import Board
from shobu.Model.Game import Game
from shobu.Model.Player import Player
from shobu.Model.constants import SQUARE_SIZE, BOARD_OUTLINE, WIDTH, GREEN, BLUE, \
    LIGHT_BROWN, DARK_BROWN, BOARD_PADDING, BLACK, DISPLAY_SIZE, WHITE, MoveDirect, \
        ROWS, COLS
from shobu.View.BoardView import BoardView

from shobu.View.GameView import GameView

FPS = 60

WIN = pygame.display.set_mode((DISPLAY_SIZE, DISPLAY_SIZE))  # Display game

# pygame.display.set_caption('Shobu')


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
                last_pos = row, col

                ''' estas 3 linhas são necessárias? '''
                board_x, board_y = selected_board.get_pos()  # gives the position of the board we are selecting with the mouse
                selected_x = board_x + (SQUARE_SIZE + BOARD_OUTLINE) * col + SQUARE_SIZE // 2
                selected_y = board_y + (SQUARE_SIZE + BOARD_OUTLINE) * row + SQUARE_SIZE // 2

                if selected_board is not None:  # Obter peça (se tiver sido selecionada alguma)
                    piece = selected_board.get_cell(row, col)  # Obter possível peça ou quadrado vazio

                    if piece != 0 and color_playing == piece.get_color():

                        pygame.draw.circle(WIN, BLUE, (selected_x, selected_y), radius)

                        player.calc_moves(selected_board, piece)  # calcular movimentos de peça escolhida
                        moves = player.get_moves()
                        previous_cell = piece.get_cell()  # guarda posição de pedra antes de a mover
                        pygame.display.update()
                        # draws the possible moves (w/ green colour) for the selected piece
                        for move in moves:
                            row, col = move
                            # Transformações dos valores para desenhar tendo em conta tada a janela do jogo
                            move_x = board_x + (SQUARE_SIZE + BOARD_OUTLINE) * col + SQUARE_SIZE // 2
                            move_y = board_y + (SQUARE_SIZE + BOARD_OUTLINE) * row + SQUARE_SIZE // 2
                            pygame.draw.circle(WIN, GREEN, (move_x, move_y), radius)
                            # refresh display

                            pygame.display.update()

                        run2 = False
                        while not run2:
                            run2 = passive_mode2(moves, selected_board, boards, piece, game_view)
                            print("SDadas")

                        game_view.draw_game()
                        pygame.display.update()
                        return
            else:
                continue


def passive_mode2(moves, board_selected, boards, piece, game_view):
    move_done_pos = []

    for event2 in pygame.event.get():
        if event2.type == pygame.QUIT:  # se clicamos para sair do jogo
            pygame.quit()
            sys.exit()  # se clicamos para sair do jogo

        elif event2.type == pygame.K_SPACE:
            return False

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
                        return True

            else:
                continue

    return False


def evaluate_move(last_pos, new_pos):           # heurística?
    info_move = []
    if new_pos[0] == last_pos[0] and new_pos[1] > last_pos:
        info_move.append(MoveDirect.right)

# def objective_test(State B|Pla|Yl|Xl)
def objective_test(boards, player):

    if player.get_color() == BLACK:
        player_to_beat_color = WHITE
    elif player.get_color() == WHITE:
        player_to_beat_color = BLACK
    else:
        # checks if a invalid player was created
        print("invalid player")
        return

    # checks if there is a board in which a player has removed all the opponent's pieces
    opponent_beaten = False
    opponent_present = False
    for board in boards:
        for row in range(ROWS):
            for col in range(COLS):

                cell_content = board.get_cell(row, col) # 0 if empty, rgb color tuple if piece is present
                if cell_content != 0:
                    if cell_content.get_color() == player_to_beat_color:
                        opponent_present = True
                        print("you haven't won to " + str(player_to_beat_color) + " in board #" + str(board.get_index()) )
                        break

            if opponent_present:
                # stops searching in this board as there is at least one opponent piece
                break

        if opponent_present == False:
            # checks if a opponent's piece WASN'T found, in the current board
            # if yes, opponent is beaten!
            opponent_beaten = True
            break
        else:
            opponent_present = False

    if opponent_beaten == True and player_to_beat_color == WHITE :
        return 1    # Player 1 wins
    elif opponent_beaten == True and player_to_beat_color == BLACK :
        return 2    # Player 2 wins
    else:
        # game not finished (should also return a 0 when it's a draw... should depend on the State?)
        return -1


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
        passive_mode1(player1, player1.get_color(), radius, run, aux_boards, game_view)
        print("out")
        res = objective_test(boards,player1)
        if res != 0:
            print("game isn't over!")

        game_view = GameView(game, WIN)
        game_view.draw_game()
        pygame.display.update()
        passive_mode1(player2, player2.get_color(), radius, run, game.get_boards(), game_view)
        res = objective_test(boards,player2)
        if res != 0:
            print("game isn't over!")


"""
    # Continuar jogo
    run = True
    while run:
        game_view.drawGame(WIN, board_view, game)

        pygame.display.update()"""

main()
