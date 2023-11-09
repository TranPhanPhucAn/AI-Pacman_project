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
            for k in range(2, 5):
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
            x = tilePacman[0][3][0]
            y = tilePacman[0][3][1]
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
            for k in range(2, 5):
                x = tilePacman[5][k][0]
                y = tilePacman[5][k][1]
                if (board[x][y] == 2):
                    heuristic += 10
                elif (board[x][y] == 3):
                    if (k == 3):
                        heuristic = -math.inf
                    else:
                        heuristic -= 50
            x = tilePacman[6][3][0]
            y = tilePacman[6][3][1]
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
            for k in range(2, 5):
                x = tilePacman[k][1][0]
                y = tilePacman[k][1][1]
                if (board[x][y] == 2):
                    heuristic += 10
                elif (board[x][y] == 3):
                    if (k == 3):
                        heuristic = -math.inf
                    else:
                        heuristic -= 50
            x = tilePacman[3][0][0]
            y = tilePacman[3][0][1]
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
            for k in range(2, 5):
                x = tilePacman[k][5][0]
                y = tilePacman[k][5][1]
                if (board[x][y] == 2):
                    heuristic += 10
                elif (board[x][y] == 3):
                    if (k == 3):
                        heuristic = -math.inf
                    else:
                        heuristic -= 50
            x = tilePacman[3][6][0]
            y = tilePacman[3][6][1]
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



def max_value(game_map, current_position, last_position, monsters, num_of_food, current_score, path_trace):
    path_trace_updated = path_trace + [current_position]

    if checkColision(current_position, monsters) or len(path_trace) > 20:
        return (current_score, path_trace_updated, "collide")

    if game_map[current_position[0]][current_position[1]] == 2:
        num_of_food -= 1
        current_score += 1
        game_map[current_position[0]][current_position[1]] = 0
        return (current_score, path_trace_updated, "found 1 food")

    if num_of_food == 0:
        return (current_score, path_trace_updated, "out of food")

    neighbors = []


    if game_map[current_position[0] - 1][current_position[1]] != 1 and game_map[current_position[0] - 1][current_position[1]] != 3:
        neighbors.append((current_position[0] - 1, current_position[1]))
    if game_map[current_position[0]][current_position[1] + 1] != 1 and game_map[current_position[0]][current_position[1] + 1] != 3:
        neighbors.append((current_position[0], current_position[1] + 1))
    if game_map[current_position[0] + 1][current_position[1]] != 1 and game_map[current_position[0] + 1][current_position[1]] != 3:
        neighbors.append((current_position[0] + 1, current_position[1]))
    if game_map[current_position[0]][current_position[1] - 1] != 1 and game_map[current_position[0]][current_position[1] - 1] != 3:
        neighbors.append((current_position[0], current_position[1] - 1))

    for m in monsters:
        for i in neighbors:
            if i[0] == m[0] and i[1] == m[1]:
                neighbors.pop(neighbors.index(i))

    if not neighbors:
        return (current_score, path_trace_updated, "no option")
    else:
        for i in neighbors:
            if i == last_position:
                neighbors.pop(neighbors.index(i))

    best_result = (-math.inf, [])
    for neighbor in neighbors:
        result = min_value(copy.deepcopy(game_map), neighbor, current_position, copy.deepcopy(monsters), num_of_food, current_score, path_trace_updated)
        if result[0] > best_result[0]:
            best_result = result
        elif result[0] == best_result[0] and len(result[1]) < len(best_result[1]):
            best_result = result
    return best_result




def min_value(game_map, current_position, last_position, monsters, num_of_food, current_score, path_trace):
    path_trace_updated = path_trace

    for i in range(len(monsters)):
        monsters[i] = monstersMove(game_map, monsters[i], current_position)

    best_result = max_value(copy.deepcopy(game_map), current_position, last_position, copy.deepcopy(monsters), num_of_food, current_score, path_trace_updated)
    return best_result
