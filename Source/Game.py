from Pacman import Pacman
from Sprite import Sprite
from Wall import Wall
from Ghost import *
from Food import Food
from constants import *


class Game:
    Wall = []
    Foods = []
    Ghosts = []
    Player = -1
    Point = 0

    def __init__(self, Matrix, pacman, monsters=[]) -> None:
        self.Player = Pacman(pacman)
        for i in monsters:
            temp = Ghost(i)
            self.Ghosts.append(temp)

        for row in range(len(Matrix)):
            for column in range(len(Matrix[row])):
                if Matrix[row][column] == 1:
                    temp = Wall((row, column))
                elif Matrix[row][column] == 2:
                    temp = Food((row, column))
                    self.Foods.append(temp)
                elif Matrix[row][column] == 3:
                    temp = Ghost((row, column))
                    self.Ghosts.append(temp)

    def checkGameFinish(self):
        isFinish = False
        if self.Player.DEAD:
            isFinish = True
            return isFinish, LOSE
        if len(self.Foods) == 0:
            isFinish = True
            return isFinish, WIN
        return isFinish, CONTINUE

    def ghostMove(self, position, idx):
        self.Ghosts[idx].changePosition(position)

    def pacmanMove(self, position):
        newPosition = position
        if (newPosition[0] - self.Player.currentPosition[0] == 1):
            self.Player.set_direction(f'../Assets/pacman_bottom.png')
        elif newPosition[0] - self.Player.currentPosition[0] == -1:
            self.Player.set_direction(f'../Assets/pacman_top.png')
        elif newPosition[1] - self.Player.currentPosition[1] == 1:
            self.Player.set_direction(f'../Assets/pacman_right.png')
        elif newPosition[1] - self.Player.currentPosition[1] == -1:
            self.Player.set_direction(f'../Assets/pacman_left.png')
        self.Player.changePosition(newPosition)

        isPacmanEatFood, foodIndex = self.checkEatFood()
        if isPacmanEatFood:
            self.Point += 20
            self.Foods.pop(foodIndex)

        self.Point -= 1

    def checkColision(self):
        for ghost in self.Ghosts:
            if ghost.currentPosition[0] == self.Player.currentPosition[0] and ghost.currentPosition[1] == \
                    self.Player.currentPosition[1]:
                return True
        return False

    def checkEatFood(self):
        for food in self.Foods:
            if food.currentPosition[0] == self.Player.currentPosition[0] and food.currentPosition[1] == \
                    self.Player.currentPosition[1]:
                return True, self.Foods.index(food)
        return False, -1

    def clearAnimation(self):
        temp = Sprite(self.Player.currentPosition)
        temp.draw()
        for ghost in self.Ghosts:
            temp.currentPosition = ghost.currentPosition
            temp.draw()
