import sys
import Menu
from level1_2 import *
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


def handle_input():
    level, map = Menu.init_menu()
    level = int(level)
    map_name = f'../Input/map{map}_level{level}.txt'

    if level not in [1, 2, 3, 4]:
        return None, None, None, None, None, None
    if map == 0 or level == 0:
        sys.exit(1)
    file = open(map_name, 'r')
    # count number of line
    cnt_line = len(file.readlines())
    file.close()

    file = open(map_name, 'r')
    MAP = []
    idx = 0
    for line in file:
        if idx == 0:
            size = line.split()
        elif idx == cnt_line - 1:
            position = line.split()
        else:
            MAP.append([int(x) for x in line.split()])
        idx += 1
    file.close()

    size_x = int(size[0])
    size_y = int(size[1])

    x = int(position[0])
    y = int(position[1])
    pos = [x, y]

    return size_x, size_y, MAP, pos, level, map_name


def menu():
    n, m, matrix, pacman, level, map_name = handle_input()
    path_ghost = None
    point = 0
    path = []
    if level == 1 or level == 2:
        path = chooseLevel(level, n, m, matrix, pacman)
    elif level == 3:
        currghost, initialghost = [], []
        food = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 3:
                    currghost.append([i + 2, j + 2])
                    initialghost.append([i + 2, j + 2])
                if matrix[i][j] == 2:
                    food += 1
        pacman[0] += 2
        pacman[1] += 2
        board = plusPadding(copy.deepcopy(matrix))
        actionsPacman, path_ghost = ingame(pacman, board, currghost, initialghost, food)
        path = []
        for item in actionsPacman:
            temp = []
            for coor in item:
                temp.append(coor - 2)
            path.append(temp)
        for i in range(len(path_ghost)):
            for j in range(len(path_ghost[i])):
                path_ghost[i][j][0] -= 2
                path_ghost[i][j][1] -= 2
        pacman[0] -= 2
        pacman[1] -= 2
    elif level == 4:

        path_file = str(map_name)
        map = readFile(path_file)  # bug here

        inf = getInfo(map)

        output = level4(map, inf[1], inf[0], pacman)
        point = output[0]
        path = output[1]
        path_ghost = output[2]

    # Trả về kích thước x, y, vị trí pacman, điểm, path_ghost, level
    return n, m, matrix, pacman, point, path, path_ghost, level


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

