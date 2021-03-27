from shobu.View.BoardView import BoardView

from shobu.Model.constants import BLACK, WHITE, OUTLINE, ROWS, COLS, SQUARE_SIZE, BOARD_OUTLINE, BOARD_PADDING, \
    LINE_HEIGHT, DISPLAY_SIZE, Action

import pygame

from shobu.View.PieceView import PieceView
from shobu.View.PlayerView import PlayerView


class GameView:

    def __init__(self, game, window_game):
        self.game = game
        self.__window_game = window_game
        self.board_view = BoardView()
        self.__player1_view = PlayerView()
        self.__player2_view = PlayerView()
        self.__piece_view = PieceView()

    def drawGame(self, window_game, board_view, game):
        # colors the screen with white
        window_game.fill(WHITE)

        # draws the rope, dividing each of the player's Homeboards
        pygame.draw.rect(window_game, BLACK, (
            BOARD_PADDING, DISPLAY_SIZE // 2 - LINE_HEIGHT // 2, DISPLAY_SIZE - 2 * BOARD_PADDING, LINE_HEIGHT))

        # desenhamos todos os tabuleiros e peças atuais
        for board in game.get_boards():
            board_view.draw(window_game, board, self.__piece_view)

        self.__player1_view.draw(window_game, game.get_player1())
        self.__player2_view.draw(window_game, game.get_player2())

    def get_next_command(self, position_mouse):
        action = Action
        run = True
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
