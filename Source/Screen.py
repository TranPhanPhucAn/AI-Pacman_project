from level3 import *
from level4 import *
from constants import *


def initGameScreen():
    pygame.init()
    pygame.display.set_caption(GAME_NAME)
    pygame.font.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(BLACK)
    clock = pygame.time.Clock()

    return screen, clock

# Set screen, game
screen, clock = initGameScreen()

def drawScore(size, game):
    text_font = pygame.font.SysFont("Comic Sans MS", 36)
    surface = pygame.Surface((10 * one_block_size, 2 * one_block_size))
    surface.fill(BLACK)
    screen.blit(surface, ((3 * one_block_size, size * one_block_size)))
    score = text_font.render(f'Score: {game.Point}', True, (255, 255, 255))
    screen.blit(score, (one_block_size, size * one_block_size))

def drawFinish(state):
    if state == WIN:
        image = pygame.image.load(r"../Assets/victory_bg.png")
        image.convert_alpha()
        image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
        image = pygame.image.load(r"../Assets/gameover_bg.png")
        image.convert_alpha()
        image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    screen.blit(image, (0, 0))

