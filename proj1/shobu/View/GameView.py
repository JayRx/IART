from shobu.View.BoardView import BoardView

from shobu.Model.constants import BLACK, WHITE, OUTLINE, ROWS, COLS, SQUARE_SIZE, BOARD_OUTLINE, BOARD_PADDING, \
    LINE_HEIGHT, DISPLAY_SIZE, Action

import pygame

from shobu.View.PieceView import PieceView


# from shobu.View.PlayerView import PlayerView


class GameView:

    def __init__(self, window_game):

        self.__window_game = window_game
        self.__board_view = BoardView()

        self.__piece_view = PieceView()

    def draw_game(self, game):
        # colors the screen with white
        self.__window_game.fill(WHITE)

        # draws the rope, dividing each of the player's Homeboards
        pygame.draw.rect(self.__window_game, BLACK, (
            BOARD_PADDING, DISPLAY_SIZE // 2 - LINE_HEIGHT // 2, DISPLAY_SIZE - 2 * BOARD_PADDING, LINE_HEIGHT))

        # desenhamos todos os tabuleiros e peças atuais
        for i in range(len(game.get_boards())):
            aux_board = game.get_boards()[i]
            self.__board_view.draw(self.__window_game, aux_board, self.__piece_view)

        pygame.display.update()
        """self.__player1_view.draw(self.__window_game, self.__game.get_player1())
        self.__player2_view.draw(self.__window_game, self.__game.get_player2())"""

    def get_next_command(self, position_mouse):
        action = Action

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # se clicamos para sair do jogo
                    action = Action.Quit
                    return action

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    action = Action.buttonDown
                    position_mouse = pygame.mouse.get_pos()
                    return action
                elif event.type == pygame.K_ESCAPE:
                    action = Action.Esc
                    return action

    def get_window_game(self):
        return self.__window_game

    def refresh_window(self):
        pygame.display.update()

    def export_game_state(self, game, mode, player_turn):
        save_file = open("save.txt", "w")
        save_file.write("mode\n")
        save_file.write(str(mode)+"\n")
        save_file.write("player_turn\n")
        save_file.write(str(player_turn)+"\n")
        save_file.write("Boards\n")
        for board in game.get_boards():
            board_content = board.get_all_board_string()
            save_file.write(str(board_content))

        save_file.close()
