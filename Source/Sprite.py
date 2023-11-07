import pygame
from constants import *
from Screen import screen


class Sprite:
    def __init__(self, position) -> None:
        self.currentPosition = position
        self.surface = pygame.Surface((one_block_size, one_block_size))
        self.surface.fill(BLACK)

    def changePosition(self, newPosition):
        if (newPosition == self.currentPosition):
            pass
        self.currentPosition = newPosition

    def draw(self):
        screen.blit(self.surface, (self.currentPosition[1] * one_block_size, self.currentPosition[0] * one_block_size))

    def display(self):
        screen.blit(self.surface, (self.currentPosition[1] * one_block_size, self.currentPosition[0] * one_block_size))
