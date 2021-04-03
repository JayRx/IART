import math

from shobu.Model.Board import Board
from shobu.Model.Player import Player

from shobu.Model.constants import *


class Heuristics:
    def __init__(self):
        self.value = 0
        pass

    def print_value(self):
        print('Heuristics Value: ' + str(self.value))

    def calc(self, boards, player):
        self.value = 0
        self.calc_number_of_pieces(boards, player)
        self.calc_position_of_pieces(boards, player)
        self.calc_agressive_position_of_pieces(boards, player)

    # Add points for every piece
    def calc_number_of_pieces(self, boards, player):
        value = 0
        for board in boards:
            for i in range(ROWS):
                for j in range(COLS):
                    cell = board.get_cell(i, j)
                    if cell != 0 and cell.get_color() == player.get_color():
                        value += 50
        self.value += math.log(value) * 100

    # Add points for every central position
    def calc_position_of_pieces(self, boards, player):
        value = 0
        for board in boards:
            for i in range(ROWS):
                for j in range(COLS):
                    cell = board.get_cell(i, j)
                    if cell != 0 and cell.get_color() == player.get_color():
                        if 1 <= i <= 2 and 1 <= j <= 2:
                            value += 50
        self.value += value * math.sqrt(3)

    # Add points for every piece with an agressive position
    def calc_agressive_position_of_pieces(self, boards, player):
        value = 0
        i_list = [-1, 0, 1]
        j_list = [-1, 0, 1]
        for board in boards:
            for i in range(ROWS):
                for j in range(COLS):
                    cell = board.get_cell(i, j)
                    if cell != 0 and cell.get_color() == player.get_color():
                        for i2 in i_list:
                            for j2 in j_list:
                                if 0 <= i + i2 < ROWS and 0 <= j + j2 < COLS and board.get_cell(i + i2, j + j2) != 0 and board.get_cell(i + i2, j + j2).get_color() != player.get_color():
                                    value += 50

                        for i2 in i_list:
                            for j2 in j_list:
                                if 0 <= i + i2 * 2 < ROWS and 0 <= j + j2 * 2 < COLS and board.get_cell(i + i2 * 2, j + j2 * 2) != 0 and board.get_cell(i + i2 * 2, j + j2 * 2).get_color() != player.get_color() and board.get_cell(i + i2,j + j2) == 0:
                                    value += 50

        self.value += value * math.sqrt(5)

def get_value(self):
        return self.value