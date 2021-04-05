import math

import pygame
import sys

from shobu.Model.Menu import Menu, main_menu

from shobu.Heuristics.Heuristics import *
from shobu.View.PlayerView import PlayerView



FPS = 60

WIN = pygame.display.set_mode((DISPLAY_SIZE, DISPLAY_SIZE))  # Display game

pygame.display.set_caption('Shobu')


def main():
    main_menu()

main()
