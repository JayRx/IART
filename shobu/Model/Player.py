from shobu.Model.constants import ROWS, COLS
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

    def agr_move_cal(self, board_to_play, vector_move, piece_to_move):
        self.restart_active_moves()
        # gets all possible aggressive moves (includes only moves to empty cells and opponent stones)
        moves = self.calc_moves2(board_to_play, piece_to_move)

        result_moves = []

        for move in moves:
            if (piece_to_move.get_row() + vector_move[0]) == move[0] and (piece_to_move.get_col() + vector_move[1]) == \
                    move[1]:
                result_moves.append(move)

        self.__aggressive_moves = result_moves

    def agr_move_cal2(self, board_to_play, vector_move, piece_to_move, color_board_played):
        self.get_agressive_moves().clear()
        if board_to_play.get_color() != color_board_played:

            # Casos de movimento , deslocamento de duas células
            if abs(vector_move[0]) > 1 or abs (vector_move[1]) > 1:
                # casos de vetor do movimento de duas casas:
                aux_vect = vector_move[0] // 2, vector_move[1] // 2
                # Três possíveis células a seguir à peça a mover
                cell1 = piece_to_move.get_row() + aux_vect[0], piece_to_move.get_col() + aux_vect[1]
                cell2 = piece_to_move.get_row() + vector_move[0], piece_to_move.get_col() + vector_move[1]
                cell3 = piece_to_move.get_row() + aux_vect[0] * 3, piece_to_move.get_col() + aux_vect[1] *3

                # Caso XO__

                if self.verify_limits(cell1) and self.verify_limits(cell2) and self.verify_limits(cell3):
                    if self.verify_is_piece_dif_color(cell1,board_to_play) and not self.verify_is_piece(
                            cell2,board_to_play) and not self.verify_is_piece(cell3,board_to_play):
                        new_local = cell2
                        self.__aggressive_moves.append(new_local)
                        return True, piece_to_move, cell1, vector_move

                # Caso XO_$, where $ is out of the board
                if self.verify_limits(cell1) and self.verify_limits(cell2) and not self.verify_limits(cell3):
                    if self.verify_is_piece_dif_color(cell1,board_to_play) and not self.verify_is_piece(cell2,board_to_play):
                        new_local = cell2
                        self.__aggressive_moves.append(new_local)
                        return True, piece_to_move, cell1, vector_move
                # Caso X_O$
                if self.verify_limits(cell1) and self.verify_limits(cell2) and not self.verify_limits(cell3):
                    if not self.verify_is_piece(cell1,board_to_play) and self.verify_is_piece_dif_color(cell2,board_to_play):
                        new_local = cell2
                        self.__aggressive_moves.append(new_local)
                        return True, piece_to_move, cell2, vector_move


                # Caso X_O_
                if self.verify_limits(cell1) and self.verify_limits(cell2) and self.verify_limits(cell3):
                    if not self.verify_is_piece(cell1,board_to_play) and self.verify_is_piece_dif_color(
                            cell2,board_to_play) and not self.verify_is_piece(cell3,board_to_play):
                        new_local = cell2
                        self.__aggressive_moves.append(new_local)

                        return True, piece_to_move, cell2, vector_move

                # Caso X__
                if self.verify_limits(cell1) and self.verify_limits(cell2):
                    if not self.verify_is_piece(cell1,board_to_play) and not self.verify_is_piece(cell2,board_to_play):
                        new_local = cell2
                        self.__aggressive_moves.append(new_local)
                        return True, piece_to_move, [], vector_move  # [] indica que não há peça do adversário a
                        # deslocar


            else:
                cell1 = piece_to_move.get_row() + vector_move[0], piece_to_move.get_col() + vector_move[1]
                cell2 = piece_to_move.get_row() + vector_move[0] * 2, piece_to_move.get_col() + vector_move[1] * 2
                # caso XO_
                if self.verify_limits(cell1) and self.verify_limits(cell2):
                    if self.verify_is_piece_dif_color(cell1,board_to_play) and not self.verify_is_piece(cell2,board_to_play):
                        new_local = cell1
                        self.__aggressive_moves.append(cell1)
                        return True, piece_to_move, cell1, vector_move

                # Caso XO$
                if self.verify_limits(cell1) and not self.verify_limits(cell2):
                    if self.verify_is_piece_dif_color(cell1,board_to_play):
                        new_local = cell1
                        self.__aggressive_moves.append(new_local)
                        return True, piece_to_move, cell1, vector_move
                        
                # Caso X_(_ ou $)
                if self.verify_limits(cell1):
                    if not self.verify_is_piece(cell1,board_to_play):
                        new_local = cell1
                        self.__aggressive_moves.append(new_local)
                        return True, piece_to_move,[], vector_move

        return False,[],[],[]

    def do_active_move(self,board, piece_to_move, adv_piece, vector_move):
        if len(adv_piece) != 0:
            new_row = adv_piece[0] + vector_move[0]
            new_col = adv_piece[1] + vector_move[1]
            piece = board.get_cell(adv_piece[0],adv_piece[1])
            if (piece != 0):
                board.change_piece_cell(piece, (new_row,new_col))

        new_row = piece_to_move.get_row() + vector_move[0]
        new_col = piece_to_move.get_col() + vector_move[1]
        board.change_piece_cell(piece_to_move,(new_row,new_col))

    def verify_limits(self, cell):
        if cell[0] > ROWS - 1 or cell[0] < 0 or cell[1] > COLS - 1 or cell[1] < 0:
            return False
        else:
            return True

    def verify_is_piece_dif_color(self, cell, board):

        if self.verify_limits(cell):
            if board.get_cell2(cell)!= 0 and board.get_cell2(cell).get_color() != self.get_color():

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

    def set_active_moves(self, active_moves):
        self.__aggressive_moves = active_moves
