from queue import PriorityQueue

def manhattan_dis(start_x, start_y, des_x, des_y):
    return (abs(des_x - start_x) + abs(start_y - des_y))