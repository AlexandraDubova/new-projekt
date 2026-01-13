import pygame
from game import Game
from pygame.locals import *


def main():
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()