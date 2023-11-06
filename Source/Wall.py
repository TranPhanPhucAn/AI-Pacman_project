import pygame
from Sprite import Sprite


class Wall(Sprite):
    def __init__(self, position) -> None:
        super().__init__(position)
        self.surface = pygame.image.load(f'../Assets/wall_img1.png')
        self.display()
