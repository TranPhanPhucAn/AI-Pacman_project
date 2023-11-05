import pygame
import sys
import copy
import time
import random
import Menu

from level1_2 import chooseLevel
from level3 import ingame, plusPadding, inputMaze
from level4 import readFile, getInfo, level4

#SET SIZE
one_block_size = 30 #pixel
SCREEN_HEIGHT = 20 * one_block_size
SCREEN_WIDTH = SCREEN_HEIGHT * 2

#SOME VARIABLE 
GAME_NAME = 'Pacman'
FPS = 30

GHOST_COLOR = (255, 0, 0) #red
PACMAN_COLOR = (255,255,0)
BLACK = (0, 0, 0)

#CheckFinish
WIN = 0
LOSE = 1
CONTINUE = 2

def initGameScreen():
    pygame.init()
    pygame.display.set_caption(GAME_NAME)
    pygame.font.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(BLACK)
    clock = pygame.time.Clock()
    
    return screen, clock

class sprite:
    def __init__(self,position) -> None:
        self.currentPosition = position
        self.surface = pygame.Surface((one_block_size,one_block_size))
        self.surface.fill(BLACK)

    def changePosition(self, newPosition):
        self.currentPosition = newPosition
    def draw(self):
        screen.blit(self.surface, (self.currentPosition[1]*one_block_size, self.currentPosition[0]*one_block_size))
    def display(self):
        screen.blit(self.surface, (self.currentPosition[1]*one_block_size, self.currentPosition[0]*one_block_size))

class Wall(sprite):
    def __init__(self, position) -> None:
        super().__init__(position)
        self.surface = pygame.image.load(f'../Assets/wall_img1.png')
        self.display()

class Ghost(sprite):
    def __init__(self, position) -> None:
        super().__init__(position)
        self.surface = pygame.image.load(f'../Assets/monster.png')
        self.display()
        

class Pacman(sprite):
    DEAD = False
    def __init__(self, position) -> None:
        super().__init__(position)
        self.surface = pygame.image.load(f'../Assets/pacman_right.png')
        self.display()
    
class Food(sprite):
    def __init__(self, position) -> None:
        super().__init__(position)
        self.surface = pygame.image.load(f'../Assets/food.png')
        self.display()

class Game:
    Foods = []
    Ghosts = []
    Player = -1
    Point = 0
    def __init__(self,Matrix,pacman) -> None:
        self.Player = Pacman(pacman)
        for row in range(len(Matrix)):
            for column in range(len(Matrix[row])):
                if Matrix[row][column] == 1:
                    temp = Wall((row,column))
                elif Matrix[row][column] == 2:
                    temp = Food((row,column))
                    self.Foods.append(temp)
                elif Matrix[row][column] == 3:
                    temp = Ghost((row,column))
                    self.Ghosts.append(temp)

    def checkGameFinish(self):
        isFinish = False
        if self.Player.DEAD:
            isFinish = True
            return isFinish, LOSE
        if len(self.Foods) == 0:
            isFinish = True
            return isFinish, WIN
        return isFinish, CONTINUE
        

    def ghostMove(self, position, idx):
        # position = functionn to move
        # print(position)
        # input(222)
        # newPosition = position
        self.Ghosts[idx].changePosition(position)

        # self.Player.DEAD = self.checkColision()
        # self.checkGameFinish()
        # self.Player.currentPosition(-1,-1)
        

    def pacmanMove(self, position):
        # position = functionn to move
        newPosition = position

        self.Player.changePosition(newPosition)

        # isPacmanEatGhost, ghostIndex = self.checkColision()
        # if isPacmanEatGhost:
        #     self.Ghosts.pop(ghostIndex)

        # isPacmanDead = self.checkColision()
        # if isPacmanDead:
        #     self.Player.DEAD = True
        #     self.checkGameFinish()

        isPacmanEatFood, foodIndex = self.checkEatFood()
        if isPacmanEatFood:
            self.Point += 20
            # self.Matrix[self.Foods[foodIndex].currentPosition[0]][self.Foods[foodIndex].currentPosition[1]] = 0
            self.Foods.pop(foodIndex)
        
        self.Point -= 1

    def checkColision(self):
        # for ghost in self.Ghosts:
        #     if ghost.currentPosition == self.Player.currentPosition:
        #         return True, self.Ghosts.index(ghost)
        # return False, -1
        for ghost in self.Ghosts:
            if ghost.currentPosition[0] == self.Player.currentPosition[0] and ghost.currentPosition[1] == self.Player.currentPosition[1]:
                return True
        return False
    
    def checkEatFood(self):
        for food in self.Foods:
            if food.currentPosition[0] == self.Player.currentPosition[0] and food.currentPosition[1] == self.Player.currentPosition[1]:
                return True, self.Foods.index(food)
        return False, -1
    
    def clearAnimation(self):
        temp = sprite(self.Player.currentPosition)
        temp.draw()
        for ghost in self.Ghosts:
            temp.currentPosition = ghost.currentPosition
            temp.draw()

def drawScore():
    text_font = pygame.font.SysFont("Arial", 36)
    surface = pygame.Surface((10*one_block_size,2*one_block_size))
    surface.fill(BLACK)
    screen.blit(surface,((3*one_block_size, m*one_block_size)))
    score = text_font.render(f'Score: {game.Point}', True, (255, 255, 255))
    screen.blit(score, (one_block_size, m*one_block_size))

def handle_input():
    level, map = Menu.init_menu()
    level = int(level)
    map_name = f'../Input/map{map}_level{level}.txt'

    if level not in [1, 2, 3, 4]:
        return None, None, None, None, None, None

    file = open(map_name, 'r')
    print(map_name)
    MAP = []
    idx = 0
    for line in file:
        if idx == 0:
            size = line.split()
        else:
            MAP.append([int(x) for x in line.split()])
        idx += 1

    file.close()
    size_x = int(size[0])
    size_y = int(size[1])
    random.seed(int(time.time()))
    x = random.randint(1, size_x - 1)
    y = random.randint(1, size_y - 1)
    while MAP[y][x] != 0 and MAP[y][x]!=2:
        x = random.randint(1, size_x - 1)
        y = random.randint(1, size_y - 1)
        print('check x:', x, 'check y:', y)
    pos = [y, x]

    return size_x, size_y, MAP, pos, level, map_name
def menu():
    n, m, matrix, pacman, level, map_name = handle_input()
    path_ghost = None
    point = 0
    path = []
    if level == 1 or level == 2:
        #cái này chỉ để lấy path thôi
        path = chooseLevel(level, n, m, matrix, pacman)
    elif level == 3:
        currghost,initialghost = [],[]
        food = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 3:
                    currghost.append([i+2,j+2])
                    initialghost.append([i+2,j+2])
                if matrix[i][j] == 2:
                    food+=1
        pacman[0] +=2
        pacman[1] +=2
        # print(pacman)
        # print(food)
        # print(currghost)
        # input("test")
        board=plusPadding(copy.deepcopy(matrix))                        #tạo padding 
        # print(board)
        # input(board)
        actionsPacman,path_ghost=ingame(pacman, board, currghost,initialghost,food)
        path = []
        for item in actionsPacman:
            temp = []
            for coor in item:
                temp.append(coor - 2)
            path.append(temp)
        for i in range(len(path_ghost)): 
            for j in range(len(path_ghost[i])):
                path_ghost[i][j][0] -=2
                path_ghost[i][j][1] -=2
        pacman[0] -=2
        pacman[1] -=2
    elif level == 4:

        path_file =  str(map_name)
        map = readFile(path_file)#bug here

        inf = getInfo(map)

        output = level4(map, inf[1], inf[0], pacman)
        point = output[0]
        path = output[1]
        path_ghost = output[2]

    #Trả về kích thước x, y, vị trí pacman, điểm, path_ghost, level
    return n, m, matrix, pacman, point, path, path_ghost, level

def drawFinish(state): 
    text_font = pygame.font.SysFont("Arial", 36)
    if state == WIN:
        image = pygame.image.load(r"../Assets/victory_bg.png")
        image.convert_alpha()
        image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # text = text_font.render("WIN", True, PACMAN_COLOR)
    else:
        image = pygame.image.load(r"../Assets/gameover_bg.png")
        image.convert_alpha()
        image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # text = text_font.render("LOSE", True, GHOST_COLOR)


    screen.blit(image, (0, 0))
    # screen.blit(text, ((n/2 - 1)*one_block_size, m*one_block_size))
    
if __name__ == "__main__":
    n, m, matrix, pacman, point, path, path_ghost, level = menu()
    SCREEN_HEIGHT = (m + 2)*one_block_size
    SCREEN_WIDTH = n*one_block_size
    screen, clock = initGameScreen()
    game = Game(matrix,pacman)
    game.Player.draw()
    drawScore()
    pygame.display.update()
    ghostmove = 0
    idx = 0
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit(0)
        for food in game.Foods:
            food.draw()  
        game.clearAnimation()
        game.pacmanMove(path[idx])
        game.Player.draw()

        game.Player.DEAD = game.checkColision()
        if game.checkColision():
            for ghost in game.Ghosts:
                ghost.draw()  
            break
        # #level để kiểm tra xem có vẽ ma hay không
        if level == 2:
            for ghost in game.Ghosts:
                ghost.draw()
        elif level == 4:
            for path_idx in range(len(game.Ghosts)):
                path_ = path_ghost[path_idx]
                game.ghostMove(path_[idx], path_idx)
                game.Ghosts[path_idx].draw()
        elif level == 3:
            for path_idx in range(len(game.Ghosts)):
                game.ghostMove(path_ghost[ghostmove][path_idx], path_idx)
                game.Ghosts[path_idx].draw()
            ghostmove += 1
        
            # print(gsm])
            # print(pacman)
            # input(1)
        
        game.Player.DEAD = game.checkColision()
        if game.checkColision():
            print(game.Player.DEAD)
            break
            
        drawScore()

        pygame.display.update()
        idx += 1

        if (idx == len(path)):
            game.Player.DEAD = game.checkColision()
            isFinsihed , state = game.checkGameFinish()
            break
                
        isFinsihed , state = game.checkGameFinish()
        if isFinsihed == True:
            break
        time.sleep(0.1)        
        clock.tick(30)

    
    drawFinish(state)
    pygame.display.update()
    time.sleep(5)
    # print(isFinsihed, state)

