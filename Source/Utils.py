import Menu
import sys
import random
import copy
import re
import Algorithm


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


def getInfo(map):
    monsters = []
    numOfFood = 0
    for x in range(len(map)):
        for y in range(len(map[x])):
            if map[x][y] == 3:
                map[x][y] = 0
                monsters.append((x, y))
            elif map[x][y] == 2:
                numOfFood += 1
    return (monsters, numOfFood)


def monstersMove(map, monsterPos, pacman):
    if monsterPos[0] == pacman[0] and monsterPos[1] == pacman[1]:
        return (monsterPos[0], monsterPos[1])

    option = []
    # thêm các ô lân cận nếu không phải tường
    if int(map[monsterPos[0] - 1][monsterPos[1]]) != 1:
        option.append((monsterPos[0] - 1, monsterPos[1]))
    if int(map[monsterPos[0]][monsterPos[1] + 1]) != 1:
        option.append((monsterPos[0], monsterPos[1] + 1))
    if int(map[monsterPos[0] + 1][monsterPos[1]]) != 1:
        option.append((monsterPos[0] + 1, monsterPos[1]))
    if int(map[monsterPos[0]][monsterPos[1] - 1]) != 1:
        option.append((monsterPos[0], monsterPos[1] - 1))

    distance = []
    for x in option:
        distance.append(((x[0] - pacman[0]) ** 2 + (x[1] - pacman[1]) ** 2))

    shortest = distance.index(min(distance))

    return option[shortest]


def checkColision(pacman, monsters):
    for m in monsters:
        if m[0] == pacman[0] and m[1] == pacman[1]:
            return True
    return False


def plusPadding(maze):
    temp = []
    for i in range(0, len(maze[0]) + 4):
        temp.append(1)
    for i in range(0, len(maze)):
        maze[i].append(1)
        maze[i].append(1)
        maze[i].insert(0, 1)
        maze[i].insert(0, 1)
    maze.append(temp)
    maze.append(temp)
    maze.insert(0, temp)
    maze.insert(0, temp)
    return maze


def createNewBoard(board, pacman):
    tileFull = []
    x = pacman[0]
    y = pacman[1]
    for i in range(-3, 4):
        tilePacman = [[x + i, y - 3], [x + i, y - 2], [x + i, y - 1], [x + i, y], [x + i, y + 1], [x + i, y + 2],
                      [x + i, y + 3]]
        tileFull.append(tilePacman)
    return tileFull


def createPacmanTile(pacman):
    i = pacman[0]
    j = pacman[1]
    maze = [[i, j - 1], [i, j + 1], [i - 1, j], [i + 1, j]]
    return maze


def availableTilePacman(board, maze, remembered):
    available = []
    direction = []
    for i in range(0, 4):
        x = maze[i][0]
        y = maze[i][1]
        # print(x,y)
        if (board[x][y] != 1):
            available.append([x, y])
            if (i == 0):
                direction.append("left")
            elif (i == 1):
                direction.append("right")
            elif (i == 2):
                direction.append("up")
            elif (i == 3):
                direction.append("down")
    return available, direction


def checkStateGame(numfood, pacman, board):
    if (numfood == 0):
        return 1
    if (board[pacman[0]][pacman[1]] == 3):
        return 2


def monsterMove(currghost, initialGhost, board):
    available = []
    available2 = []
    newpos = []
    oldpos = copy.deepcopy(currghost)
    for index in range(0, len(currghost)):
        i = currghost[index][0]
        j = currghost[index][1]
        initialX = initialGhost[index][0]
        initialY = initialGhost[index][1]
        if (i == initialX and j == initialY):
            available.append([i - 1, j])
            available.append([i + 1, j])
            available.append([i, j - 1])
            available.append([i, j + 1])
        elif (i == initialX + 1 or i == initialX - 1):
            available.append([initialX, initialY])
        elif (j == initialY - 1 or j == initialY + 1):
            available.append([initialX, initialY])
        for k in range(0, len(available)):
            x = available[k][0]
            y = available[k][1]
            if (board[x][y] != 1):
                available2.append([x, y])
        if (len(available2) > 1):
            randomchoice = random.randint(0, len(available2) - 1)
        else:
            randomchoice = 0
        randomVal = available2[randomchoice]
        available2.clear()
        available.clear()
        newpos.append(randomVal)
    return newpos, oldpos
