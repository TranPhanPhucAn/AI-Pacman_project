import pygame
from Sprite import Sprite


class Food(Sprite):
    def __init__(self, position) -> None:
        super().__init__(position)
        self.surface = pygame.image.load(f'../Assets/food.png')
        self.draw()
