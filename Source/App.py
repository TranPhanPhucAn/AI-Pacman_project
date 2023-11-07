from Sprite import Sprite
from Game import Game
from Screen import *
import time
from Algorithm import *
from utils import *

class App:
    def __init__(self):
        n, m, matrix, pacman, point, path, path_ghost, level = show(self)
        if m is None or n is None:
            sys.exit(1)
        screen, clock = initGameScreen()
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
        food = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 3:
                    currghost.append([i + 2, j + 2])
                    initialghost.append([i + 2, j + 2])
                if matrix[i][j] == 2:
                    food += 1
        pacman[0] += 2
        pacman[1] += 2
        board = plusPadding(copy.deepcopy(matrix))
        actionsPacman, path_ghost = ingame(pacman, board, currghost, initialghost, food)
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

        output = level4(map, inf[1], inf[0], pacman)
        point = output[0]
        path = output[1]
        path_ghost = output[2]
        return path
def show(App: App):
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
        path = App.level4(matrix, pacman)


    # Trả về kích thước x, y, vị trí pacman, điểm, path_ghost, level
    return n, m, matrix, pacman, point, path, path_ghost, level