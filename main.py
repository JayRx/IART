import math

import pygame
import time
import sys

from shobu.Model.Menu import Menu, main_menu

from shobu.Heuristics.Heuristics import *
from shobu.View.PlayerView import PlayerView
from shobu.Model.Board import Board
from shobu.Model.Game import Game
from shobu.Model.Player import Player, player_play
from shobu.View.BoardView import BoardView

from shobu.View.GameView import GameView
from shobu.Controller.GameController import GameController
from shobu.View.PlayerView import PlayerView
from minimax_algorithm import Minimax



FPS = 60

WIN = pygame.display.set_mode((DISPLAY_SIZE, DISPLAY_SIZE))  # Display game

pygame.display.set_caption('Shobu')


def main():
    main_menu()

main()
