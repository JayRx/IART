from enum import Enum

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 4, 4
SQUARE_SIZE = WIDTH / COLS / 4

BOARD_PADDING = 50
BOARD_OUTLINE = 2
LINE_HEIGHT = 4

# Cores em formato RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (245, 222, 179)
DARK_BROWN = (139, 69, 19)
OUTLINE = (210, 180, 140)
LIGHT_BROWN = (205, 133, 63)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VIOLET = (199, 21, 133)

# Piece
PADDING = 10
OUTLINE = 2

DISPLAY_SIZE = WIDTH - WIDTH // 3 + BOARD_PADDING // 2


class Action(Enum):
    buttonDown = 1
    Esc = 2
    Quit = 3
