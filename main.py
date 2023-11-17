import pygame
import os
from os import path
import math
import pickle

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
n = 0
game_over = 0
DoneDead = False
main_menu = True
level = 1

# Surfaces
player_surf = pygame.image.load("graphics/White_square.png")
bg = pygame.image.load(os.path.join("graphics/Dungeon_Backgrond_1.png")).convert()
bg = pygame.transform.scale(bg, (scr_width, scr_height))
tiles = math.ceil(scr_width / bg.get_width()) + 1
restart_img = pygame.image.load("graphics/Tileset/Buttons/reset_button.png")
start_img = pygame.image.load("graphics/Tileset/Buttons/start_btn.png")
exit_img = pygame.image.load("graphics/Tileset/Buttons/exit_btn.png")


bgx = 0
bgx2 = bg.get_width()

# Rects
player_rect = player_surf.get_rect()
bg_rect = bg.get_rect()

# test world map
# world_data = [
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     [1, 0, 0, 0, 0, 5, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
#     [1, 0, 0, 0, 0, 0, 1, 1, 1, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1],
#     [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# ]


def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, white, (0, line * tile_size), (scr_width, line * tile_size))
        pygame.draw.line(screen, white, (line * tile_size, 0), (line * tile_size, scr_height))


# Classes

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        # mouse position
        pos = pygame.mouse.get_pos()

        # check click
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # button drawing
        screen.blit(self.image, self.rect)
        return action


class Player():
    def __init__(self, x, y):
        self.images_idle = []
        self.images_right = []
        self.images_left = []
        self.images_death = []
        self.index = 0
        self.counter = 0
        self.deathcounter = 0
        for n in range(0, 4):
            img_idle = pygame.image.load(f"graphics/Sprites/Player/slime-idle-{n}.png")
            img_idle = pygame.transform.scale(img_idle, (45, 37))
            img_right = pygame.image.load(f"graphics/Sprites/Player/slime-move-{n}.png")
            img_right = pygame.transform.scale(img_right, (45, 37))
            img_left = pygame.transform.flip(img_right, True, False)
            img_dead = pygame.image.load(f"graphics/Sprites/Player/slime-die-{n}.png")
            img_dead = pygame.transform.scale(img_dead, (45, 37))
            self.images_idle.append(img_idle)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
            self.images_death.append(img_dead)

        # Player image loading to rect
        self.image = self.images_idle[self.index]
        self.rect = self.image.get_rect()
        # Player coordinate passing
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    # def movement(self):
    #
    #     dx = 0
    #     dy = 0

    # # Keypresses
    # key = pygame.key.get_pressed()
    # if key[pygame.K_LEFT] or key[pygame.K_a]:
    #     dx -= 5
    #     self.counter += 1
    #     self.direction = 1
    # if key[pygame.K_RIGHT] or key[pygame.K_d]:
    #     dx += 5
    #     self.counter += 1
    #     self.direction = 1
    # if key[pygame.K_SPACE] and self.jumped == False:
    #     self.vel_y = -11
    #     self.jumped = True
    # if not key[pygame.K_SPACE]:
    #     self.jumped = False
    #
    # # gravity
    # self.vel_y += 1
    # if self.vel_y > 10:
    #     self.vel_y = 10
    # dy += self.vel_y
    #
    #
    # for tile in world.tile_list:
    #
    #     # X collision
    #     if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
    #         dx = 0
    #
    #     # Y collision
    #     if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
    #         # Top collision
    #         if self.vel_y < 0:
    #             dy = tile[1].bottom - self.rect.top
    #             self.vel_y = 0
    #         # Bottom collision
    #         elif self.vel_y >= 0:
    #             dy = tile[1].top - self.rect.bottom
    #             self.vel_y = 0
    #
    # # Enemy collision
    # if pygame.sprite.spritecollide(self, batGroup, False):
    #     game_over = True
    #
    # # Player position
    # self.rect.x += dx
    # self.rect.y += dy

    def animation(self):

        self.counter += 1
        if self.counter > 5:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_idle):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            elif self.direction == 0:
                self.image = self.images_idle[self.index]

    def update(self, game_over):

        global DoneDead
        dx = 0
        dy = 0

        if game_over == 0:

            # movement
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
            if key[pygame.K_SPACE] or key[pygame.K_w] or key[pygame.K_UP] and self.jumped == False:
                self.vel_y = -11
                self.jumped = True
            if key[pygame.K_l]:
                self.direction = 2
            if not key[pygame.K_SPACE]:
                self.jumped = False

            # gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            for tile in world.tile_list:

                # X collision
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                # Y collision
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # Top collision
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # Bottom collision
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0

            # Enemy collision
            if pygame.sprite.spritecollide(self, batGroup, False):
                game_over = True

            if pygame.sprite.spritecollide(self, spikeGroup, False):
                game_over = True

            # Player position
            self.rect.x += dx
            self.rect.y += dy
            player.animation()

        else:
            if not DoneDead:
                self.deathcounter += 1
                if self.deathcounter == 5:
                    self.image = self.images_death[0]
                elif self.deathcounter == 10:
                    self.image = self.images_death[1]
                elif self.deathcounter == 15:
                    self.image = self.images_death[2]
                elif self.deathcounter >= 20:
                    self.image = self.images_death[3]
                    DoneDead = True

        # Draw the player
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, white, self.rect, 1)

        return game_over

    def reset(self, x, y):
        self.images_idle = []
        self.images_right = []
        self.images_left = []
        self.images_death = []
        self.index = 0
        self.counter = 0
        self.deathcounter = 0
        for n in range(0, 4):
            img_idle = pygame.image.load(f"graphics/Sprites/Player/slime-idle-{n}.png")
            img_idle = pygame.transform.scale(img_idle, (45, 37))
            img_right = pygame.image.load(f"graphics/Sprites/Player/slime-move-{n}.png")
            img_right = pygame.transform.scale(img_right, (45, 37))
            img_left = pygame.transform.flip(img_right, True, False)
            img_dead = pygame.image.load(f"graphics/Sprites/Player/slime-die-{n}.png")
            img_dead = pygame.transform.scale(img_dead, (45, 37))
            self.images_idle.append(img_idle)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
            self.images_death.append(img_dead)

        # Player image loading to rect
        self.image = self.images_idle[self.index]
        self.rect = self.image.get_rect()
        # Player coordinate passing
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0


class World():
    def __init__(self, data):
        self.tile_list = []

        border = pygame.image.load("graphics/Tileset/tile000.png")

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
                if tile == 2:
                    bat = Enemy(column_count * tile_size, row_count * tile_size - 6)
                    batGroup.add(bat)
                if tile == 3:
                    spike = Spike(column_count * tile_size, row_count * tile_size + (tile_size // 2))
                    spikeGroup.add(spike)
                if tile == 5:
                    exittile = Exit(column_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exitGroup.add(exittile)
                column_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("graphics/Sprites/Enemy/tile034.png")
        self.image = pygame.transform.scale(self.image, (55, 55))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.posCounter = 0

    def update(self):
        self.rect.x += self.direction
        self.posCounter += 1
        pygame.draw.rect(screen, white, self.rect, 1)
        if abs(self.posCounter) > 50:
            self.direction *= -1
            self.posCounter *= -1


class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("graphics/Tileset/tile038.png")
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.posCounter = 0

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("graphics/Tileset/Buttons/exit.png")
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


player = Player(98, (scr_height - 93))
batGroup = pygame.sprite.Group()
spikeGroup = pygame.sprite.Group()
exitGroup = pygame.sprite.Group()

# Load level data
# if path.exists(f"World_Data/level{level}_data"):
#     pickle_input = open(f"World_Data/level{level}_data", "r")
# world_data = pickle.load(pickle_input)

if path.exists(f"World_Data/level{level}_data"):
    fo = open(f"World_Data/level{level}_data", "r")
world_data = []
world_data = fo.read()
world = World(world_data)

restart_button = Button(scr_width // 2, scr_height // 2 + 25, restart_img)
start_button = Button(scr_width // 2 - 125, scr_height // 2 - 200, start_img)
exit_button = Button(scr_width // 2 - 105, scr_height // 2 + 100, exit_img)

# Setting the exit condition
gameover = False
menu = True

# While loop for active game
while not gameover:
    clock.tick(clock_speed)
    # Main loop for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True

        # Testing screenshot function
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                pygame.image.save(screen, f"graphics/screenshot{n}.png")
                n += 1
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

    if main_menu:
        if exit_button.draw():
            gameover = True
        if start_button.draw():
            main_menu = False
    else:
       # print(world_data)
        world.draw()
        if game_over == 0:
            batGroup.update()
        batGroup.draw(screen)
        spikeGroup.draw(screen)
        exitGroup.draw(screen)
        draw_grid()
        game_over = player.update(game_over)


        if game_over == 1:
            if restart_button.draw():
                player.reset(98, (scr_height - 93))
                game_over = False

    # Screen updating
    pygame.display.flip()

pygame.quit()