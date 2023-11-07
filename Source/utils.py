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