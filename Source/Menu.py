import pygame
import sys

one_block_size = 30
SCREEN_HEIGHT = 20 * one_block_size
SCREEN_WIDTH = SCREEN_HEIGHT * 2

def init_menu():
    window_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Menu")
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    BLACK = (0, 0, 0)

    home_background = pygame.image.load(r"../Assets/bg.png")
    home_background.convert_alpha()
    home_background = pygame.transform.scale(home_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    font = pygame.font.init()
    font = pygame.font.SysFont("Arial", 36)

    menu_items = ["Play", "About us", "Exit"]
    level_items = ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Return']
    list_members = [
        '21120407 - Tran Phan Phuc An',
        '21120409 - Nguyen Duc Duy Anh',
        '21120423 - Pham Manh Cuong',
        '21120451 - Le Bao Hieu',
        '21120539 - Tran Minh Quang',
        'Return'
    ]
    map_items = ['Map 1', 'Map 2', 'Return']

    arrow = pygame.Surface((20, 20), pygame.SRCALPHA)
    pygame.draw.polygon(arrow, YELLOW, [(0, 0), (20, 10), (0, 20)])

    def draw_list(list_item, selected_item):
        for i, item in enumerate(list_item):
            text = font.render(item, True, YELLOW if i == selected_item else WHITE)
            text_rect = text.get_rect()
            text_rect.center = (window_size[0] // 2, window_size[1] // 1.75 + i * 40)
            screen.blit(text, text_rect)
            if i == selected_item:
                screen.blit(arrow, (text_rect[0] - 30, text_rect[1] + 10))
        pygame.display.update()

    def menu_list(list_item, level=0, map=0):
        selected_item = 0
        running = True

        while running:
            # print(level,map)
            if level != 0 and map != 0:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_item = (selected_item - 1) % len(list_item)
                    elif event.key == pygame.K_DOWN:
                        selected_item = (selected_item + 1) % len(list_item)
                    elif event.key == pygame.K_RETURN:
                        if selected_item == len(list_item) - 1:
                            running = False
                        if list_item == menu_items:
                            if selected_item == 0:
                                level, map = menu_list(level_items, level, map)
                            elif selected_item == 1:
                                menu_list(list_members, level, map)
                        elif list_item == level_items:
                            if selected_item != len(level_items) - 1:
                                level = level_items[selected_item].split(' ')[1]
                                level, map = menu_list(map_items, level, map)

                        elif list_item == map_items:
                            if selected_item != len(map_items) - 1:
                                map = map_items[selected_item].split(' ')[1]

            screen.fill(BLACK)
            screen.blit(home_background, (0, 0))
            draw_list(list_item, selected_item)

        return level, map
    return menu_list(menu_items)