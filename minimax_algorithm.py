from copy import deepcopy
from shobu.State.State import State
from shobu.Model.constants import BLACK, WHITE

# import rgb colors?

class Minimax:
    def __init__(self, player):
        self.player = player

    # depth - depth of the search tree
    def minimax(boards, depth, max_player, game_controller)
        # in depth 0 of the tree
        if self.depth == 0 or game_controller.objective_test(boards, max_player) != -1:
            # this means that in this board, we have a winner
            return heuristics.calc(boards, self.player).value, boards    #TODO rever um pouco isto (max player e boards finais(criar uma nova var no State?))
        
        if max_player:
            maxVal = float('-inf')
            best_turn = None
            for turn in self.get_all_turns(game_controller, WHITE, self.player, boards):
                # gets an evaluation for each of the turns
                evaluation = minimax(turn, depth-1, False, game_controller)[0]  # here only max_evalue is needed
                max_evalue = max(max_evalue, evaluation)

                if max_evalue == evaluation:
                    # saves the turn for this case (the one that generates the best evaluation)
                    best_turn = turn

            return max_evalue, best_turn
            
        else: #for min_player (max_player == False)

            minVal = float('inf')
            best_turn = None
            for turn in self.get_all_turns(game_controller, BLACK, self.player, boards):
                # gets an evaluation for each of the turns
                evaluation = minimax(turn, depth-1, True, game_controller)[0]  # here only min_evalue is needed
                min_evalue = min(min_evalue, evaluation)

                if min_evalue == evaluation:
                    # saves the turn for this case (the one that generates the best evaluation)
                    best_turn = turn

            return min_evalue, best_turn

    def generate_turn(self, boards, pieces, move_vector, game):
        board_passive, board_aggressive = boards
        piece_passive, piece_aggressive = pieces

        board_passive.change_piece_cell(piece_passive, move_vector)
        board_aggressive.change_piece_cell(piece_aggressive, move_vector)
        
        return boards

    def get_all_turns(self, game, color, player, boards):
        turns = []  # list of various "minimax states"

        for board_passive in player.get_boards():

            # for each of player's color pieces, in each (passive) board 
            for piece_passive in board_passive.get_all_pieces(color):

                # gets all possible passive moves for that piece
                passive_moves = player.calc_moves(board_passive, piece_passive)
                # gets color of chosen board for passive move
                board_passive_color = board_passive.get_color() 

                for pas_move in passive_moves:

                    # for each possible board of aggressive move (has to be board of opposite color)
                    for board_aggressive in game.obtain_opposite_color_boards(board_passive_color):
                        move_vector = pas_move[0] - piece_passive.get_row(), pas_move[1] - piece_passive.get_col()

                        # for each piece of the player playing an aggressive move
                        for piece_aggressive in board_aggressive.get_all_pieces(color)
                            # compute and gets an aggressive move
                            player.agr_move_cal(board_aggressive, move_vector, piece_aggressive)
                            aggressive_move = player.get_agressive_moves()
                        
                            # creates a copy of the boards being considered
                            temp_board_passive = deepcopy(board_passive)
                            temp_board_aggressive = deepcopy(board_aggressive)
                            temp_boards = temp_board_passive, temp_board_aggressive

                            temp_piece_passive = temp_board_passive.get_cell(piece_passive.get_row(), piece_passive.get_col()) #has to be != 0
                            temp_piece_aggressive = temp_board_aggressive.get_cell(piece_aggressive.get_row(), piece_aggressive.get_col()) #has to be != 0
                            temp_pieces = temp_piece_passive, temp_piece_aggressive

                            # generates a new boards (passive+aggressive) for each possible turn, saves it as a MinimaxState
                            possible_play_boards = generate_turn(temp_boards, temp_pieces, move_vector, game)
                            turn = MinimaxState(game, boards, possible_play_boards, pieces)    # boards represents what is being displayed now, before the move (board untouched)
                            
                            # appends the turn that can be done with that pieces, giving as result possible_play_boards
                            turns.append(turn)

        return turns