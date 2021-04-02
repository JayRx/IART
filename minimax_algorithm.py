from copy import deepcopy

# import rgb colors?

class Minimax:
    def __init__(self, depth):
        self.depth = depth

    # depth - depth of the search tree
    def minimax(board, max_player, game_controller)  # maybe boards?
        # in depth 0 of the tree
        if self.depth == 0 or game_controller.objective_test(board, max_player) != -1:
            # this means that in this board, we have a winner
            return heuristics.calc(board, max_player).value, board
        
        if max_player:
            maxVal = float('-inf')
            best_turn = None
            # for turn in get_all_turns()
            #...
        else: #for min_player
            #...

    def generate_turn(self, piece, board, move_vector, game):
        board.change_piece_cell(piece, move_vector)
        return board

    def get_all_turns(self, game, color, player, board):        #we must do this for 2 boards at the same time
        turns = []

        for piece in game.get_all_pieces(color):
            # gets all possible passive moves for that piece (one of the boards)
            passive_moves = player.calc_moves(board, piece)

            for pas_move in passive_moves:
                move_vector = pas_move[0] - piece.get_row(), pas_move[1] - piece.get_col()  # vector do movimento
                # here we have to change board (maybe?)
                aggressive_move = player.agr_move_cal(board, move_vector, piece)
                
                temporary_board = deepcopy(board)
                # generates a new board for each possible turn
                possible_board = generate_turn(piece, temporary_board, move_vector, game)
                # appends the turn that can be done with that piece, giving as result possible_board 
                turns.append([possible_board, piece])

        return turns