import pygame
import os
import sys
import math

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
clock = pygame.time.Clock()
clock_speed = 30
scroll = 0

# Surfaces
player_surf = pygame.image.load("graphics/White_square.png")
bg = pygame.image.load(os.path.join("graphics/Dungeon_Backgrond_1.png")).convert()
bg = pygame.transform.scale(bg, (scr_width, scr_height))
tiles = math.ceil(scr_width / bg.get_width()) + 1

bgx = 0
bgx2 = bg.get_width()

# Rects
player_rect = player_surf.get_rect()
bg_rect = bg.get_rect()

# test world map
world_data = [
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
        pygame.draw.line(screen, white, (0, line * tile_size), (scr_width, line * tile_size))
        pygame.draw.line(screen, white, (line * tile_size, 0), (line * tile_size, scr_height))


# Classes

class Player():
    def __init__(self, x, y):
        self.images_idle = []
        self.images_right = []
        self.images_left = []
        self.images_jump = []
        self.index = 0
        self.counter = 0
        for n in range(0, 4):
            img_idle = pygame.image.load(f"graphics/Sprites/slime-idle-{n}.png")
            img_idle = pygame.transform.scale(img_idle, (55, 70))
            img_right = pygame.image.load(f"graphics/Sprites/slime-move-{n}.png")
            img_right = pygame.transform.scale(img_right, (55, 70))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_idle.append(img_idle)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        # Player image loading to rect
        self.image = self.images_idle[self.index]
        self.rect = self.image.get_rect()
        # Player coordinate passing
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def movement(self):

        dx = 0
        dy = 0

        # Keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            dx -= 5
            self.counter += 1
            self.direction = 1
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            dx += 5
            self.counter += 1
            self.direction = 1
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -10
            self.jumped = True
        if not key[pygame.K_SPACE]:
            self.jumped = False

        # gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Player position
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > (scr_height - tile_size):
            self.rect.bottom = (scr_height - tile_size)

    def animation(self):
        self.counter += 1
        if self.counter > 5:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_idle):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            else:
                self.image = self.images_idle[self.index]


    def update(self):

        # Draw the player
        screen.blit(self.image, self.rect)

        # movement
        player.movement()
        player.animation()

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


player = Player(98, (scr_height - 118))
world = World(world_data)


# Setting the exit condition
game_over = False
menu = True

# While loop for active game
while not game_over:
    clock.tick(clock_speed)
    # Main loop for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        # Testing screenshot function
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                pygame.image.save(screen, "graphics/screenshot.png")

    while menu:

        i = 0
        while i < tiles:
            screen.blit(bg, (bg.get_width() * i + scroll, 0))
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        menu = False

        scroll -= 0.08

        if abs(scroll) > bg.get_width():
            scroll = 0
        pygame.display.flip()


    # Screen clearing
    screen.fill(black)
    world.draw()
    draw_grid()
    player.update()

    # Screen updating
    pygame.display.flip()

pygame.quit()
