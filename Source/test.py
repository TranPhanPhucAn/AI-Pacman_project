import pygame
import sys
import math

pygame.init()

# Cấu hình cửa sổ trò chơi
window_size = (400, 400)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pac-Man Menu")

# Màu sắc
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Tạo đối tượng Font
font = pygame.font.Font(None, 36)

# Tạo các mục menu
menu_items = ["New Game", "Options", "Quit"]
selected_item = 0

# Tạo đối tượng mũi tên (dấu mũi tên bằng pygame)
arrow = pygame.Surface((20, 20), pygame.SRCALPHA)
pygame.draw.polygon(arrow, YELLOW, [(0, 0), (10, 20), (20, 0)])

# Tọa độ trung tâm của menu
center_x, center_y = window_size[0] // 2, window_size[1] // 2
radius = 100

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_item = (selected_item - 1) % len(menu_items)
            elif event.key == pygame.K_DOWN:
                selected_item = (selected_item + 1) % len(menu_items)
            elif event.key == pygame.K_RETURN:
                if selected_item == 0:  # New Game
                    print("Starting a new game")
                elif selected_item == 1:  # Options
                    print("Opening options")
                elif selected_item == 2:  # Quit
                    running = False

    # Xóa cửa sổ trò chơi
    screen.fill(BLACK)

    # Vẽ Pac-Man (menu)
    angle = 45  # Góc mở miệng
    for i, item in enumerate(menu_items):
        text = font.render(item, True, YELLOW if i == selected_item else WHITE)
        text_rect = text.get_rect()
        x = center_x + int(radius * math.cos(math.radians(angle)))
        y = center_y + int(radius * math.sin(math.radians(angle)))
        text_rect.center = (x, y)
        screen.blit(text, text_rect)
        if i == selected_item:
            # Vẽ dấu mũi tên bên cạnh mục menu đang được chọn
            screen.blit(arrow, (x + 50, y - 10))
        angle += 90  # Di chuyển đến mục menu tiếp theo

    # Cập nhật cửa sổ
    pygame.display.update()

pygame.quit()
sys.exit()
