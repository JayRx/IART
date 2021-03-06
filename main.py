import pygame
from shobu.constants import ROWS, COLS, SQUARE_SIZE, BOARD_OUTLINE, WIDTH, HEIGHT, BACKGROUND, RED, GREEN, BLUE, LIGHT_BROWN, DARK_BROWN, WHITE, BOARD_PADDING, BLACK, LINE_HEIGHT
from shobu.board import Board

FPS = 60
DISPLAY_SIZE = WIDTH - WIDTH // 3 + BOARD_PADDING // 2
WIN = pygame.display.set_mode((DISPLAY_SIZE, DISPLAY_SIZE))
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
    return row, col

def main():
    selected_x, selected_y = None, None
    prev_selected_piece = None
    selected_board = None
    selected_cell = None
    radius = SQUARE_SIZE // 2 - 10

    run = True
    clock = pygame.time.Clock()

    WIN.fill(WHITE)
    pygame.draw.rect(WIN, BLACK, (BOARD_PADDING, DISPLAY_SIZE // 2 - LINE_HEIGHT // 2, DISPLAY_SIZE - 2 * BOARD_PADDING, LINE_HEIGHT))

    boards = [Board(0, 0, DARK_BROWN, 0), Board(0, 1, LIGHT_BROWN, 1), Board(1, 0, DARK_BROWN, 2), Board(1, 1, LIGHT_BROWN, 3)]

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                selected_board = get_board_hover_mouse(boards, pos)
                selected_x = None
                selected_y = None
                if selected_board != None:
                    cell = get_cell_hover_mouse(selected_board, pos)
                    board_x, board_y = selected_board.get_pos()
                    row, col = cell
                    row, col = int(row), int(col)
                    if 0 <= row < ROWS:
                        if 0 <= col < COLS:
                            selected_x = board_x + (SQUARE_SIZE + BOARD_OUTLINE) * col + SQUARE_SIZE // 2
                            selected_y = board_y + (SQUARE_SIZE + BOARD_OUTLINE) * row + SQUARE_SIZE // 2
                            selected_cell = row, col
                            selected_cell_aux = [row, col]
                            if prev_selected_piece != None and prev_selected_piece != 0:
                                print(prev_selected_piece.get_moves())
                                if selected_cell_aux in prev_selected_piece.get_moves():
                                    selected_board.change_piece_cell(prev_selected_piece, selected_cell)
                                    selected_cell, selected_x, selected_y, prev_selected_piece = None, None, None, None
                            prev_selected_piece = board.get_cell(row, col)
                else:
                    prev_selected_piece = None

        for board in boards:
            board.draw(WIN)
            if selected_x != None and selected_y != None:
                row, col = selected_cell
                row = int(row)
                col = int(col)
                piece = board.get_cell(row, col)
                if piece != 0:
                    pygame.draw.circle(WIN, BLUE, (selected_x, selected_y), radius)
                    moves = piece.get_moves()
                    board_x, board_y = selected_board.get_pos()
                    for move in moves:
                        row, col = move
                        move_x = board_x + (SQUARE_SIZE + BOARD_OUTLINE) * col + SQUARE_SIZE // 2
                        move_y = board_y + (SQUARE_SIZE + BOARD_OUTLINE) * row + SQUARE_SIZE // 2
                        pygame.draw.circle(WIN, GREEN, (move_x, move_y), radius)
                else:
                    pygame.draw.circle(WIN, RED, (selected_x, selected_y), radius)

        pygame.display.update()

    pygame.quit()

main()
