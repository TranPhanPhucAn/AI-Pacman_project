from Sprite import Sprite
from Game import Game
from Screen import *

if __name__ == "__main__":
    n, m, matrix, pacman, point, path, path_ghost, level = menu()
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

        if level == 2:
            for ghost in game.Ghosts:
                ghost.draw()
        elif level == 4:
            for path_idx in range(len(game.Ghosts)):
                path_ = path_ghost[path_idx]
                game.ghostMove(path_[idx], path_idx)
                game.Ghosts[path_idx].draw()
        elif level == 3:
            for path_idx in range(len(game.Ghosts)):
                game.ghostMove(path_ghost[ghostmove][path_idx], path_idx)
                game.Ghosts[path_idx].draw()
            ghostmove += 1

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

    drawFinish(state)
    pygame.display.update()
    time.sleep(5)
