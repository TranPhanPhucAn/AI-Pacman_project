import random
import re
import math
import copy

"""
    Level 3: Pac-man cannot see the foods if they are outside Pacman’s nearest threestep.
    It means that Pac-man just only scan all the adjacent him (8 tiles x 3).
    There are many foods in the map.
    Monsters just move one step in any valid direction (if any) around the initial location at the start of the game.
    Each step Pacman go, each step Monsters move.
"""
def inputMaze(filename):
    f = open(filename, mode='r')
    content = f.readline()
    size = re.findall(r'\d+', content)
    n = int(size[0])
    m = int(size[1])
    # print(n,m)
    maze = []
    for i in range(0, m):
        content = f.readline()
        arrNum = re.findall(r'\d+', content)
        llen = len(arrNum)
        for j in range(0, llen):
            arrNum[j] = int(arrNum[j])
        maze.append(arrNum)
    content = f.readline()
    size = re.findall(r'\d+', content)
    initialX = int(size[0])
    initialY = int(size[1])
    return maze, initialX, initialY, m, n


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


def heurisicValue(tilePacman, board, direction):
    heuristicVal = []
    for i in range(0, len(direction)):
        heuristic = 0
        if (direction[i] == "up"):
            for k in range(2, 5):
                x = tilePacman[2][k][0]
                y = tilePacman[2][k][1]
                if (board[x][y] == 2):
                    heuristic += 35
                elif (board[x][y] == 3):
                    heuristic = -math.inf
            for k in range(1, 6):
                x = tilePacman[1][k][0]
                y = tilePacman[1][k][1]
                if (board[x][y] == 2):
                    heuristic += 10
                elif (board[x][y] == 3):
                    if (k == 3):
                        heuristic = -math.inf
                    else:
                        # print("sssss")
                        heuristic -= 50
            for k in range(0, 7):
                x = tilePacman[0][k][0]
                y = tilePacman[0][k][1]
                if (board[x][y] == 2):
                    heuristic += 5
                elif (board[x][y] == 3):
                    heuristic -= 100
        elif (direction[i] == "down"):
            for k in range(2, 5):
                x = tilePacman[4][k][0]
                y = tilePacman[4][k][1]
                if (board[x][y] == 2):
                    heuristic += 35
                elif (board[x][y] == 3):
                    heuristic = -math.inf
            for k in range(1, 6):
                x = tilePacman[5][k][0]
                y = tilePacman[5][k][1]
                if (board[x][y] == 2):
                    heuristic += 10
                elif (board[x][y] == 3):
                    if (k == 3):
                        heuristic = -math.inf
                    else:
                        # print("sssss")
                        heuristic -= 50
            for k in range(0, 7):
                x = tilePacman[6][k][0]
                y = tilePacman[6][k][1]
                if (board[x][y] == 2):
                    heuristic += 5
                elif (board[x][y] == 3):
                    heuristic -= 100
        elif (direction[i] == "left"):
            # print("ddddd")
            for k in range(2, 5):
                x = tilePacman[k][2][0]
                y = tilePacman[k][2][1]
                if (board[x][y] == 2):
                    heuristic += 35
                elif (board[x][y] == 3):
                    heuristic = -math.inf
            for k in range(1, 6):
                x = tilePacman[k][1][0]
                y = tilePacman[k][1][1]
                if (board[x][y] == 2):
                    heuristic += 10
                elif (board[x][y] == 3):
                    if (k == 3):
                        heuristic = -math.inf
                    else:
                        heuristic -= 50
            for k in range(0, 7):
                x = tilePacman[k][0][0]
                y = tilePacman[k][0][1]
                if (board[x][y] == 2):
                    heuristic += 5
                elif (board[x][y] == 3):
                    heuristic -= 100
        elif (direction[i] == "right"):
            for k in range(2, 5):
                x = tilePacman[k][4][0]
                y = tilePacman[k][4][1]
                if (board[x][y] == 2):
                    heuristic += 35
                elif (board[x][y] == 3):
                    heuristic = -math.inf
            for k in range(1, 6):
                x = tilePacman[k][5][0]
                y = tilePacman[k][5][1]
                if (board[x][y] == 2):
                    heuristic += 10
                elif (board[x][y] == 3):
                    if (k == 3):
                        heuristic = -math.inf
                    else:
                        heuristic -= 50
            for k in range(0, 7):
                x = tilePacman[k][6][0]
                y = tilePacman[k][6][1]
                if (board[x][y] == 2):
                    heuristic += 5
                elif (board[x][y] == 3):
                    heuristic -= 100
        heuristicVal.append(heuristic)
    return heuristicVal


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


def localsearch(board, pacman, remembered, visited):
    mazePacman = createPacmanTile(pacman)
    tilePacman = createNewBoard(board, pacman)
    available, direction = availableTilePacman(board, mazePacman, remembered)
    heuristicVal = heurisicValue(tilePacman, board, direction)
    countVisited = 0
    count = []
    for i in range(0, len(available)):
        if (remembered[0] == available[i][0] and remembered[1] == available[i][1]):
            countVisited += 1000
        for j in range(0, len(visited)):  # [[f,f],[ff]]
            if (visited[j][0] == available[i][0] and visited[j][1] == available[i][1]):
                # print("co chay")
                countVisited += 1
            else:
                countVisited += 0
        count.append(countVisited)
        countVisited = 0
    for i in range(0, len(direction)):
        heuristicVal[i] -= count[i]

    maxheuristic = max(heuristicVal)
    index = heuristicVal.index(maxheuristic)
    remembered[0] = pacman[0]
    remembered[1] = pacman[1]
    return available[index], remembered


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


def ingame(pacman, board, currghost, initialghost, numfood):
    actionsForPacman = []
    actionsForGhost = []
    visited = []
    actionPacman = copy.deepcopy(pacman)
    remembered = copy.deepcopy(pacman)
    recursion = 0
    while (True):
        visited.append(actionPacman)
        actionPacman, remembered = localsearch(board, actionPacman, remembered, visited)
        actionsForPacman.append(actionPacman)
        oldpos = copy.deepcopy(currghost)
        actionGhost, oldpos = monsterMove(currghost, initialghost, board)
        actionsForGhost.append(actionGhost)
        for i in range(0, len(actionGhost)):
            x = actionGhost[i][0]
            y = actionGhost[i][1]
            currghost[i][0] = x
            currghost[i][1] = y
            board[x][y] = 3
            board[oldpos[i][0]][oldpos[i][1]] = 0
        if (board[actionPacman[0]][actionPacman[1]] == 2):
            numfood -= 1
            board[actionPacman[0]][actionPacman[1]] = 0
        checkGame = checkStateGame(numfood, actionPacman, board)
        if (checkGame == 1):
            return actionsForPacman, actionsForGhost
        elif (checkGame == 2):
            return actionsForPacman, actionsForGhost
        recursion += 1
    return actionsForPacman, actionsForGhost
