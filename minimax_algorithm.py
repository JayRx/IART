from copy import deepcopy
from shobu.State.State import State

# import rgb colors?

class Minimax:
    def __init__(self, depth):
        self.depth = depth

    # depth - depth of the search tree
    def minimax(boards, max_player, game_controller)
        # in depth 0 of the tree
        if self.depth == 0 or game_controller.objective_test(boards, max_player) != -1:
            # this means that in this board, we have a winner
            return heuristics.calc(boards, max_player).value, boards
        
        if max_player:
            maxVal = float('-inf')
            best_turn = None
            #for turn in get_all_turns(): 
            #...
        else: #for min_player
            #...

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
                            temp_boards = deepcopy(board_passive, board_aggressive)
                            pieces = piece_passive, piece_aggressive    #not sure if I have to deepcopy here too

                            # generates a new boards (passive+aggressive) for each possible turn, saves it as a MinimaxState
                            possible_play_boards = generate_turn(temp_boards, pieces, move_vector, game)
                            turn = MinimaxState(game, boards, possible_play_boards, pieces)    # boards represents what is being displayed now, before the move (board untouched)
                            
                            # appends the turn that can be done with that pieces, giving as result possible_play_boards
                            turns.append(turn)

        return turns