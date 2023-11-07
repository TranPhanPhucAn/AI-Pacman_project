from queue import PriorityQueue
import copy
from utils import *
import math


def manhattan_dis(start_x, start_y, des_x, des_y):
    return (abs(des_x - start_x) + abs(start_y - des_y))


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