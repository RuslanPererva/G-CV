import os

import pygame


def __init__(self, img):
    pygame.sprite.Sprite.__init__(self)
    self.sprite = img
    self.sprite.set_colorkey(BLACK)
    self.speedx = 0
    self.speedy = 0
    self.rect = self.sprite.get_rect()
    self.radius = 18
    self.rect.centerx = WIDTH / 2
    self.rect.bottom = HEIGHT - 25