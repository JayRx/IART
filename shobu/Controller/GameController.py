from shobu.Controller.PlayerController import PlayerController
from shobu.Model.constants import BLACK, WHITE, ROWS, COLS


class GameController:

    def __init__(self, game, game_view):
        self.__game = game
        self.__game_view = game_view
        self.__player1_controller = PlayerController(game, game_view)
        self.__player2_controller = PlayerController(game, game_view)

    def start(self):
        self.__game_view.draw_game()

    # def objective_test(State B|Pla|Yl|Xl)
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
            return 1    # Player 1 wins
        elif opponent_beaten == True and player_to_beat_color == BLACK :
            return 2    # Player 2 wins
        else:
            # game not finished
            return -1

