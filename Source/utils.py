import Menu
import sys
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