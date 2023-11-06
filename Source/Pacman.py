import pygame
from Sprite import Sprite


class Pacman(Sprite):
    DEAD = False

    def __init__(self, position) -> None:
        super().__init__(position)
        self.display()

    def set_direction(self, path):
        self.surface = pygame.image.load(path)
        self.display()
