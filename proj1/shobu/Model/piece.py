

class Piece:


    def __init__(self, row, col, color):
        # posição na matriz identificativa do board
        self.__row = row
        self.__col = col
        self.__color = color

        # posição no board, tendo em conta o ecrã
        self.__x_in_board = 0
        self.__y_in_board = 0

    def __repr__(self):
        return str(self.__color)

    def set_x_in_board(self, x):
        self.__x_in_board = x

    def set_y_in_board(self, y):
        self.__y_in_board = y

    def get_cell(self):
        return self.__row, self.__col

    def set_cell(self, cell):
        self.__row, self.__col = cell

    def get_color(self):
        return self.__color

    def get_x_in_board(self):
        return self.__x_in_board

    def get_y_in_board(self):
        return self.__y_in_board

    def get_row(self):
        return self.__row

    def get_col(self):
        return self.__col