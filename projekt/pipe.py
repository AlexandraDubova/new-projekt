import pygame
from settings import *

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position, speed, gap):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/pipe.png")
        self.rect = self.image.get_rect()
        self.speed = speed
        self.gap = gap 
        #pozice 1 je pro horni rouru, -1 pro dolni
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y]
        elif position == -1:
            self.rect.topleft = [x, y]

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()