from queue import PriorityQueue
import copy
from Utils import *
import math


def manhattan_dis(start_x, start_y, des_x, des_y):
    return (abs(des_x - start_x) + abs(start_y - des_y))


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


# hàm max cỉa minimax
def pacmanMove_max(map, currentPos, lastPos, monsters, numOfFood, score, trace):
    trace2 = copy.deepcopy(trace)
    trace2.append(currentPos)  # thêm vào mảng trace để trả về kết quả cuối cùng

    # nếu trong các lựa chọn để đi có đụng monster
    if checkColision(currentPos, monsters) or len(trace) > 20:
        return (score, trace2, "collide")

    if map[currentPos[0]][currentPos[1]] == 2:
        numOfFood -= 1
        score += 1
        map[currentPos[0]][currentPos[1]] = 0
        return (score, trace2, "found 1 food")

    if numOfFood == 0:
        return (score, trace2, "out of food")

    option = []  # các lựa chọn để đi
    # thêm các ô lân cận nếu không phải tường và quái vật
    if map[currentPos[0] - 1][currentPos[1]] != 1 and map[currentPos[0] - 1][currentPos[1]] != 3:
        option.append((currentPos[0] - 1, currentPos[1]))
    if map[currentPos[0]][currentPos[1] + 1] != 1 and map[currentPos[0]][currentPos[1] + 1] != 3:
        option.append((currentPos[0], currentPos[1] + 1))
    if map[currentPos[0] + 1][currentPos[1]] != 1 and map[currentPos[0] + 1][currentPos[1]] != 3:
        option.append((currentPos[0] + 1, currentPos[1]))
    if map[currentPos[0]][currentPos[1] - 1] != 1 and map[currentPos[0]][currentPos[1] - 1] != 3:
        option.append((currentPos[0], currentPos[1] - 1))

    for m in monsters:
        for i in option:
            if i[0] == m[0] and i[1] == m[1]:
                option.pop(option.index(i))

    if not option:
        return (score, trace2, "no option")
    else:
        for i in option:
            if i == lastPos:
                option.pop(option.index(i))

    # trả về option đi để có điểm lớn nhất
    result = (-math.inf, [])
    for x in option:
        output = pacmanMove_min(copy.deepcopy(map), x, currentPos, copy.deepcopy(monsters), numOfFood, score, trace2)
        if output[0] > result[0]:
            result = output
        elif output[0] == result[0] and len(output[1]) < len(result[1]):
            result = output

    return result


# hàm min của minimax
def pacmanMove_min(map, currentPos, lastPos, monsters, numOfFood, score, trace):
    trace2 = copy.deepcopy(trace)

    for i in range(len(monsters)):  # cập nhật lại vị trí mới của quái vật trong mảng monster
        monsters[i] = monstersMove(map, monsters[i], currentPos)

    result = pacmanMove_max(copy.deepcopy(map), currentPos, lastPos, copy.deepcopy(monsters), numOfFood, score, trace2)
    return result
