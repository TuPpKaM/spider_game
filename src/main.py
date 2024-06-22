import sys

import pygame

from game import Game
from settings import *


def main():
    pygame.init()

    game = Game()
    game.run()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
