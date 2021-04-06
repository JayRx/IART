from copy import deepcopy
from shobu.State.State import State, MinimaxState
from shobu.Model.constants import BLACK, WHITE, SQUARE_SIZE, BOARD_OUTLINE
from shobu.Heuristics.Heuristics import Heuristics


class Minimax:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        globals.initialize()
        print(globals.it)

    # depth - depth of the search tree
    def minimax(self, boards, depth, max_player, game_controller, alpha, beta):
        globals.it += 1
        # in depth 0 of the tree
        if depth == 0 or game_controller.objective_test(boards, self.player2) != -1:
            # this means that in this board, we have a winner
            heuristics = Heuristics()
            heuristics.calc(boards, self.player2)
            return heuristics.get_value(), boards  # TODO rever um pouco isto (max player )

        if max_player:
            max_evalue = float('-inf')
            best_turn = None
            for turn in self.get_all_turns(game_controller, self.player2.get_color(), self.player2, boards):
                new_boards = turn.get_boards_after_play()
                # gets an evaluation for each of the turns
                evaluation = self.minimax(new_boards, depth - 1, False, game_controller, alpha, beta)[
                    0]  # here only max_evalue is needed
                max_evalue = max(max_evalue, evaluation)
                alpha = max(alpha, max_evalue)

                if max_evalue == evaluation:
                    # saves the turn for this case (the one that generates the best evaluation)
                    best_turn = new_boards

                if beta <= alpha:
                    break

            return max_evalue, best_turn

        else:  # for min_player (max_player == False)

            min_evalue = float('inf')
            best_turn = None
            for turn in self.get_all_turns(game_controller, self.player1.get_color(), self.player1, boards):
                new_boards = turn.get_boards_after_play()
                # gets an evaluation for each of the turns
                evaluation = self.minimax(new_boards, depth - 1, True, game_controller, alpha, beta)[
                    0]  # here only min_evalue is needed
                min_evalue = min(min_evalue, evaluation)
                beta = min(beta, min_evalue)

                if min_evalue == evaluation:
                    # saves the turn for this case (the one that generates the best evaluation)
                    best_turn = new_boards

                if beta <= alpha:
                    break

            return min_evalue, best_turn

    def generate_turn(self, player, boards, pieces, adv_piece, move_vector, game):
        board_passive, board_aggressive = boards
        piece_passive, piece_aggressive = pieces

        destination_cell_passive = piece_passive.get_row() + move_vector[0], piece_passive.get_col() + move_vector[1]

        board_passive.change_piece_cell(piece_passive, destination_cell_passive)
        player.do_active_move(board_aggressive, piece_aggressive, adv_piece, move_vector)

        return boards

    def get_all_turns(self, game, color, player, boards):
        turns = []  # list of various "minimax states"

        for board_passive in player.get_boards():

            # for each of player's color pieces, in each (passive) board 
            for piece_passive in board_passive.get_all_pieces(color):

                # gets color of chosen board for passive move
                board_passive_color = board_passive.get_color()

                # gets all possible passive moves for that piece
                passive_moves = player.calc_moves(board_passive, piece_passive)

                for pas_move in passive_moves:

                    # for each possible board of aggressive move (has to be board of opposite color)
                    for board_aggressive in game.obtain_opposite_color_boards(board_passive_color):

                        move_vector = pas_move[0] - piece_passive.get_row(), pas_move[1] - piece_passive.get_col()

                        # for each piece of the player playing an aggressive move (in one of the boards)
                        for piece_aggressive in board_aggressive.get_all_pieces(color):
                            # compute and gets an aggressive move
                            res_calc_aggressive = player.active_move(board_aggressive, move_vector, piece_aggressive,
                                                                     board_passive_color)
                            # saves if there's an adversary piece removed with this movement
                            adv_piece = res_calc_aggressive[2]

                            # creation of temporary copies (board+pieces)
                            # creates a copy of the boards being considered
                            temp_board_passive = deepcopy(board_passive)
                            temp_board_aggressive = deepcopy(board_aggressive)
                            temp_boards = temp_board_passive, temp_board_aggressive

                            temp_piece_passive = temp_board_passive.get_cell(piece_passive.get_row(),
                                                                             piece_passive.get_col())
                            temp_piece_aggressive = temp_board_aggressive.get_cell(piece_aggressive.get_row(),
                                                                                   piece_aggressive.get_col())
                            temp_pieces = temp_piece_passive, temp_piece_aggressive

                            # generates a new boards (passive+aggressive) for each possible turn, saves it as a MinimaxState
                            possible_play_boards = self.generate_turn(player, temp_boards, temp_pieces, adv_piece,
                                                                      move_vector, game)
                            turn = MinimaxState(game, boards, possible_play_boards,
                                                temp_pieces)  # boards represents what is being displayed now, before the move (board untouched)

                            # appends the turn that can be done with that pieces, giving as result possible_play_boards
                            turns.append(turn)

        return turns
