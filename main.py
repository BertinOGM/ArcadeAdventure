import pygame

# Initializing Pygame
pygame.init()

# Initializing the screen
scr_width = 1000
scr_height = 600
screen = pygame.display.set_mode((scr_width, scr_height))
pygame.display.set_caption("Platformer")

# Constants
white = (255, 255, 255)
black = (0, 0, 0)
tile_size = 50
keys = pygame.key.get_pressed()

# test world map
world_data =[
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, white, (0, line * tile_size), (scr_width, line* tile_size))
        pygame.draw.line(screen, white, (line * tile_size, 0), (line * tile_size, scr_height))

# Classes

class Player():
    def __init__(self, x, y):
        img = pygame.image.load("graphics/White_square.png")
        img_rect = img.get_rect()

class World():
    def __init__(self, data):
        self.tile_list = []

        border = pygame.image.load("graphics/Wall_brick.png")

        row_count = 0
        for row in data:
            column_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(border, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                column_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


world = World(world_data)
# Surfaces
player_surf = pygame.image.load("graphics/White_square.png")

# Rects
player_rect = player_surf.get_rect()

# Setting the exit condition
game_over = False

# While loop for active game
while not game_over:
    # Main loop for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        # Testing screenshot function
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                pygame.image.save(screen, "graphics/screenshot.png")

    # Screen clearing
    screen.fill(black)
    world.draw()
    draw_grid()

    # Screen updating
    pygame.display.flip()


pygame.quit()
