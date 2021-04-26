import math




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

        for board in boards:
            for i in range(ROWS):
                for j in range(COLS):
                    cell = board.get_cell(i, j)
                    if cell != 0 and cell.get_color() != player.get_color():
                        value -= 50

        self.value += value * 10

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
        self.value += value

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

        self.value += value

    def get_value(self):
        return self.value




    def objective_test(self, boards, player):

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
                    # stops searching in this board as there is, at least, one opponent piece
                    break

            if opponent_present == False:
                # checks if a opponent's piece WASN'T found, in the current board
                # if yes, opponent is beaten!
                opponent_beaten = True
                break
            else:
                opponent_present = False

        if opponent_beaten == True and player_to_beat_color == WHITE :
            print("Player1 Wins!")
            return 1    # Player 1 wins
        elif opponent_beaten == True and player_to_beat_color == BLACK :
            print("Player2 Wins!")
            return 2    # Player 2 wins
        else:
            # game not finished
            return -1
