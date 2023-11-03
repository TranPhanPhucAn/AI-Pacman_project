import pygame
import sys
import main

pygame.init()

# Cấu hình cửa sổ trò chơi
window_size = (main.SCREEN_WIDTH, main.SCREEN_HEIGHT)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Simple Menu")

# Màu sắc
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
RED = (255, 0, 0)

# Tạo đối tượng Font
font = pygame.font.Font(None, 36)

# Tạo đối tượng menu
menu_items = ["Level", "Members", "Exit"]
level_items = ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Return']
map_items = ['Map 1', 'Map 2', 'Return']

selected_item = 0
def draw_item(list_item, selected_item):
    for i, item in enumerate(list_item):
        text = font.render(item, True, RED if i == selected_item else GRAY)
        text_rect = text.get_rect()
        text_rect.center = (window_size[0] // 2, window_size[1] // 2 + i * 40)
        screen.blit(text, text_rect)

    # Cập nhật cửa sổ
    pygame.display.update()

level = 0
map = 0
map_name = f'../Input/map{map}_level{level}.txt'


def handle_event(event, selected_item):

def menu(list_item, selected_item, level, map):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(list_item)
                elif event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(list_item)
                elif event.key == pygame.K_RETURN:

                    if selected_item == 0:  # Start
                        if list_item == menu_items:
                            menu(level_items, selected_item, level, map)
                        elif list_item == level_items:
                            menu(map_items, selected_item, level, map)
                    elif selected_item == 1:  # Options
                        print("Members")
                    elif selected_item == len(list_item) - 1:  # Quit
                        running = False

        # Xóa cửa sổ trò chơi
        screen.fill(WHITE)

        # Vẽ các mục menu
        draw_item(list_item, selected_item)
    return level, map

level, map = menu(menu_items, selected_item, level, map)

pygame.quit()
sys.exit()
