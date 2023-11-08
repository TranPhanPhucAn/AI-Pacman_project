from Sprite import Sprite
from Game import Game
from Screen import *
import time
from Algorithm import *
from Utils import *


class App:
    def __init__(self):
        a = process(self)
        n = a[0]
        m = a[1]
        matrix = a[2]
        pacman = a[3]
        point = a[4]
        path = a[5]
        path_ghost = a[6]
        level = a[7]
        if level == 4:
            monsters = a[8]
        if m is None or n is None:
            sys.exit(1)
        screen, clock = initGameScreen()
        if level == 4:
            game = Game(matrix, pacman, monsters)
        else:
            game = Game(matrix, pacman)
        game.Player.draw()
        drawScore(m, game)
        pygame.display.update()
        ghostmove = 0
        idx = 0
        print('Running process:')
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit(0)
            for food in game.Foods:
                food.draw()

            old_pacman_position = game.Player.currentPosition
            game.clearAnimation()
            game.pacmanMove(path[idx])
            game.Player.draw()
            old_pacman_sprite = Sprite(old_pacman_position)
            old_pacman_sprite.draw()

            game.Player.DEAD = game.checkColision()
            if game.checkColision():
                for ghost in game.Ghosts:
                    ghost.draw()
                break
            if level == 1:
                pass
            if level == 2:
                for ghost in game.Ghosts:
                    ghost.draw()
            elif level == 3:
                for path_idx in range(len(game.Ghosts)):
                    game.ghostMove(path_ghost[ghostmove][path_idx], path_idx)
                    game.Ghosts[path_idx].draw()
                ghostmove += 1
            elif level == 4:
                for path_idx in range(len(game.Ghosts)):
                    path_ = path_ghost[path_idx]
                    game.ghostMove(path_[idx], path_idx)
                    game.Ghosts[path_idx].draw()

            game.Player.DEAD = game.checkColision()
            if game.checkColision():
                break
            drawScore(m, game)
            pygame.display.update()
            idx += 1
            if (idx == len(path)):
                game.Player.DEAD = game.checkColision()
                isFinsihed, state = game.checkGameFinish()
                break

            isFinsihed, state = game.checkGameFinish()
            if isFinsihed == True:
                break
            time.sleep(0.1)
            clock.tick(30)
        print(path)
        drawFinish(state)
        pygame.display.update()
        time.sleep(5)

    def detec_food(self, MAP, size_x, size_y):
        for i in range(size_y):
            for j in range(size_x):
                if MAP[i][j] == 2:
                    return (i, j)

    def level1(self, MAP, pos, size_x, size_y):
        visited = []
        path = []
        temp_path = {}
        queue = PriorityQueue()
        beg = (pos[0], pos[1])
        end = self.detec_food(MAP, size_x, size_y)
        queue.put((manhattan_dis(pos[0], pos[1], end[0], end[1]), beg))
        cost = {}
        cost[beg] = 0
        while queue != None:
            v = queue.get()[1]
            visited.append(v)
            neighbor = []
            if (v == end):
                path.append(v)
                while v != beg:
                    v = temp_path[v]
                    path.append(v)
                path.reverse()
                return path
            if v[0] - 1 >= 0 and MAP[v[0] - 1][v[1]] != 1:
                neighbor_cur = (v[0] - 1, v[1])
                neighbor.append(neighbor_cur)
            if v[0] + 1 < size_y - 1 and MAP[v[0] + 1][v[1]] != 1:
                neighbor_cur = (v[0] + 1, v[1])
                neighbor.append(neighbor_cur)
            if v[1] - 1 >= 0 and MAP[v[0]][v[1] - 1] != 1:
                neighbor_cur = (v[0], v[1] - 1)
                neighbor.append(neighbor_cur)
            if v[1] + 1 < size_x - 1 and MAP[v[0]][v[1] + 1] != 1:
                neighbor_cur = (v[0], v[1] + 1)
                neighbor.append(neighbor_cur)
            for item in neighbor:
                if item not in visited:
                    cost[item] = cost[v] + 1
                    queue.put((cost[item] + manhattan_dis(item[0], item[1], end[0], end[1]), item))
                    temp_path[item] = v

    def level2(self, MAP, pos, size_x, size_y):
        visited = []
        path = []
        temp_path = {}
        queue = PriorityQueue()
        beg = (pos[0], pos[1])
        end = self.detec_food(MAP, size_x, size_y)
        queue.put((manhattan_dis(pos[0], pos[1], end[0], end[1]), beg))
        cost = {}
        cost[beg] = 0
        while queue != None:
            v = queue.get()[1]
            visited.append(v)
            neighbor = []
            if (v == end):
                path.append(v)
                while v != beg:
                    v = temp_path[v]
                    path.append(v)
                path.reverse()
                return path
            if v[0] - 1 >= 0 and MAP[v[0] - 1][v[1]] != 1 and MAP[v[0] - 1][v[1]] != 3:
                neighbor_cur = (v[0] - 1, v[1])
                neighbor.append(neighbor_cur)
            if v[0] + 1 < size_y - 1 and MAP[v[0] + 1][v[1]] != 1 and MAP[v[0] + 1][v[1]] != 3:
                neighbor_cur = (v[0] + 1, v[1])
                neighbor.append(neighbor_cur)
            if v[1] - 1 >= 0 and MAP[v[0]][v[1] - 1] != 1 and MAP[v[0]][v[1] - 1] != 3:
                neighbor_cur = (v[0], v[1] - 1)
                neighbor.append(neighbor_cur)
            if v[1] + 1 < size_x - 1 and MAP[v[0]][v[1] + 1] != 1 and MAP[v[0]][v[1] + 1] != 3:
                neighbor_cur = (v[0], v[1] + 1)
                neighbor.append(neighbor_cur)
            for item in neighbor:
                if item not in visited:
                    cost[item] = cost[v] + 1
                    queue.put((cost[item] + manhattan_dis(item[0], item[1], end[0], end[1]), item))
                    temp_path[item] = v

    def level3(self, matrix, pacman):
        currghost, initialghost = [], []
        numfood = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 3:
                    currghost.append([i + 2, j + 2])
                    initialghost.append([i + 2, j + 2])
                if matrix[i][j] == 2:
                    numfood += 1
        pacman[0] += 2
        pacman[1] += 2
        board = plusPadding(copy.deepcopy(matrix))

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

        actionsPacman, path_ghost = ingame(pacman, board, currghost, initialghost, numfood)

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
        return path, path_ghost

    def level4(self, map, pacman):
        inf = getInfo(map)
        monsters = inf[0]
        numOfFood = inf[1]
        map_copy = copy.deepcopy(map)
        monstersPos = copy.deepcopy(monsters)  # không làm ảnh hưởng mảng gốc

        # khởi tạo mảng để lưu bước đi của monster
        monstersMoveList = []
        if monsters:
            for i in range(len(monsters)):
                monstersMoveList.append([])
                monstersMoveList[i].append(monsters[i])
        pacmanMoveList = [pacman]
        numEaten = 0
        while numOfFood > 0:
            output = pacmanMove_max(map_copy, pacmanMoveList[-1], pacmanMoveList[-1], monstersPos, numOfFood, 0, [])
            if not output[1]:
                print("stop by break")
                break

            numOfFood -= output[0]

            numEaten += output[0]

            temp = output[1].pop(0)
            pacmanMoveList = pacmanMoveList + output[1]
            for p in output[1]:
                for m in range(len(monstersMoveList)):
                    monstersMoveList[m].append(monstersMove(map, monstersMoveList[m][-1], p))
            for y in range(len(monstersMoveList)):
                monstersPos[y] = monstersMoveList[y][-1]

            map_copy = copy.deepcopy(map)
            for x in pacmanMoveList:
                map_copy[x[0]][x[1]] = 0

            if output[2] == "collide":
                break

            if output[2] == "no option":
                pacmanMoveList = pacmanMoveList + [temp]
                for m in range(len(monstersMoveList)):
                    monstersMoveList[m].append(monstersMove(map, monstersMoveList[m][-1], temp))

                break
        point = numEaten
        path = pacmanMoveList
        path_ghost = monstersMoveList
        return path, path_ghost, point, monsters


def process(App: App):
    n, m, matrix, pacman, level, map_name = handle_input()
    path_ghost = None
    point = 0
    path = []
    if level == 1:
        path = App.level1(matrix, pacman, n, m)
    elif level == 2:
        path = App.level2(matrix, pacman, n, m)
    elif level == 3:
        path, path_ghost = App.level3(matrix, pacman)
    elif level == 4:
        path, path_ghost, point, monsters = App.level4(matrix, pacman)
        return [n, m, matrix, pacman, point, path, path_ghost, level, monsters]

    return [n, m, matrix, pacman, point, path, path_ghost, level]
