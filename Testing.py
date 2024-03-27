import pygame
import os
from os import path
import math
import pickle
from pygame import mixer

# initialising
pygame.init()
mixer.init()

scr_width = 1000
scr_height = 600
screen = pygame.display.set_mode((scr_width, scr_height))
pygame.display.set_caption('My Game')
clock = pygame.time.Clock()
clock_speed = 60
scroll = [0, 0, 0, 0, 0, 0]
tile_size = 50
level = 0
max_levels = 5
score = 0
game_state = 0
exitListX = []
exitListY = []
white = (255, 255, 255)
black = (0, 0, 0)

# Font
font_1 = pygame.font.SysFont('Roboto', 60)
font_2 = pygame.font.SysFont('Roboto', 25)
font_3 = pygame.font.Font('Fonts/StayPixelRegular-EaOxl.ttf', 75)

# Surfaces
bg = pygame.image.load(os.path.join("graphics/Dungeon_Background_3.png")).convert()
bg = pygame.transform.scale(bg, (scr_width, scr_height))
scroll_math = math.ceil(scr_width / bg.get_width()) + 1
background_pillar = pygame.image.load('graphics/Background/Background_Pillars.png')
background_pillar = pygame.transform.scale(background_pillar, (scr_width, scr_height))
background_1 = pygame.image.load('graphics/Background/Background_1.png')
background_1 = pygame.transform.scale(background_1, (scr_width, scr_height))


# Load sounds
gameover_sound = pygame.mixer.Sound('Sounds/gameover.wav')
gameover_sound.set_volume(0.3)
jump_sound = pygame.mixer.Sound('Sounds/jump.wav')
coin_sound = pygame.mixer.Sound('Sounds/coin.wav')
coin_sound.set_volume(0.5)

bg_images = []
for i in range(7, 0, -1):
    bg_image = pygame.transform.scale((pygame.image.load(f'graphics/Background/{i}.png').convert_alpha()),
                                      (scr_width, scr_height))
    bg_images.append(bg_image)


def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, white, (0, line * tile_size), (scr_width, line * tile_size))
        pygame.draw.line(screen, white, (line * tile_size, 0), (line * tile_size, scr_height))


def reset_level(level):
    exitListY.clear()
    exitListX.clear()
    player.reset(98, (scr_height - 93))
    enemyGroup.empty()
    spikeGroup.empty()
    exitGroup.empty()
    if path.exists(f"World_Data/level{level}_data.txt"):
        pickle_in = open(f"World_Data/level{level}_data.txt", "rb")
        world_data = pickle.load(pickle_in)
    world = World(world_data)

    return world


def draw_text(text, font, colour, x, y):
    img = font.render(text, True, colour)
    screen.blit(img, (x, y))


class Button():
    def __init__(self, x, y, image, scale):
        self.image = image
        self.image = pygame.transform.scale_by(self.image, scale)
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
        self.reset(x, y)

    def animation(self):
        self.counter += 1
        if self.counter > 10:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_idle):
                self.index = 0
            if self.direction == 0:
                self.image = self.images_idle[self.index]
            elif self.direction == 1:
                self.image = self.images_right[self.index]
            elif self.direction == 2:
                self.image = self.images_death[self.index]

    def reset(self, x, y):
        self.images_idle = []
        self.images_right = []
        self.images_left = []
        self.images_jump = []
        self.images_death = []
        self.index = 0
        self.counter = 0
        self.deathCounter = 0
        for n in range(0, 4):
            img_idle = pygame.image.load(f"graphics/Sprites/Player/slime-idle-{n}.png")
            img_idle = pygame.transform.scale(img_idle, (45, 37))
            img_right = pygame.image.load(f"graphics/Sprites/Player/slime-move-{n}.png")
            img_right = pygame.transform.scale(img_right, (45, 37))
            img_dead = pygame.image.load(f"graphics/Sprites/Player/slime-die-{n}.png")
            img_dead = pygame.transform.scale(img_dead, (45, 37))
            self.images_idle.append(img_idle)
            self.images_right.append(img_right)
            self.images_death.append(img_dead)
        self.image = self.images_idle[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.air = 0
        self.direction = 0
        self.doneDead = False

    def update(self, game_state):

        if game_state == 0:
            player.animation()
            dx = 0
            dy = 0

            # movement
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] or key[pygame.K_a]:
                dx -= 5
                self.direction = 1
            if key[pygame.K_RIGHT] or key[pygame.K_d]:
                dx += 5
                self.direction = 1
            if key[pygame.K_SPACE] and self.jumped == False and self.air == 0:
                self.vel_y = -10
                self.jumped = True
                self.air = 1
                jump_sound.play()
            if not key[pygame.K_SPACE]:
                if not key[pygame.K_RIGHT] and not key[pygame.K_d] and not key[pygame.K_LEFT] and not key[pygame.K_a]:
                    self.direction = 0
                self.jumped = False

            # gravity
            self.vel_y += 0.5
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
                        self.air = 0

            # Enemy collision
            if pygame.sprite.spritecollide(self, enemyGroup, False):
                game_state = -1
                gameover_sound.play()
            elif pygame.sprite.spritecollide(self, spikeGroup, False):
                game_state = -1
                gameover_sound.play()

            self.rect.x += dx
            self.rect.y += dy

        elif game_state == -1:
            if not self.doneDead:
                self.deathCounter += 1
                if self.deathCounter == 5:
                    self.image = self.images_death[0]
                elif self.deathCounter == 10:
                    self.image = self.images_death[1]
                elif self.deathCounter == 15:
                    self.image = self.images_death[2]
                elif self.deathCounter > 20:
                    self.image = self.images_death[3]
                    self.DoneDead = True

        screen.blit(self.image, self.rect)

        return game_state


class World():
    def __init__(self, data):
        self.tile_list = []

        floor1 = pygame.image.load('graphics/New Tile/Tiles/Floor1.png')
        floor2 = pygame.image.load('graphics/New Tile/Tiles/Floor2.png')
        wall1 = pygame.image.load('graphics/New Tile/Tiles/Bricks1.png')
        wall2 = pygame.image.load('graphics/New Tile/Tiles/Bricks2.png')

        row_count = 0
        for row in data:
            column_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(floor1, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 6:
                    img = pygame.transform.scale(wall2, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    enemy = Enemy(column_count * tile_size, row_count * tile_size + 5)
                    enemyGroup.add(enemy)
                if tile == 3:
                    spike = Spike(column_count * tile_size, row_count * tile_size + (tile_size // 2))
                    spikeGroup.add(spike)
                if tile == 4:
                    coin = Coin(column_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coinGroup.add(coin)
                if tile == 5:
                    exittile = Exit(column_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exitGroup.add(exittile)
                    exits = pygame.sprite.spritecollide(exittile, exitGroup, False)
                    for exitSprite in exits:
                        exitListX.append(exitSprite.rect.x)
                        exitListY.append(exitSprite.rect.y)
                column_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("graphics/Sprites/Enemy/tile034.png")
        self.image = pygame.transform.scale(self.image, (45, 45))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.temp = 0

    def update(self):
        if self.temp < 45:
            self.rect.x += 1
            self.temp += 1
        if self.temp >= 45:
            self.rect.x -= 1
            self.temp += 1
        if self.temp >= 90:
            self.temp = 0


class Spike(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("graphics/Tileset/tile038.png")
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("graphics/Tileset/Buttons/exit.png")
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("graphics/Tileset/tile015.png")
        self.image = pygame.transform.scale(self.image, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


player = Player(98, (scr_height - 92))
enemyGroup = pygame.sprite.Group()
spikeGroup = pygame.sprite.Group()
coinGroup = pygame.sprite.Group()
exitGroup = pygame.sprite.Group()

# Load level data
if path.exists(f"World_Data/level{level}_data.txt"):
    pickle_in = open(f"World_Data/level{level}_data.txt", "rb")
    world_data = pickle.load(pickle_in)
world = World(world_data)

# buttonsD
restart_button = Button(scr_width // 2, scr_height // 2 + 25,
                        pygame.image.load("graphics/Tileset/Buttons/reset_button.png"), 1)
start_button = Button(scr_width // 2 - 103, scr_height // 2 - 150,
                      (pygame.image.load('graphics/Tileset/Buttons/Play_Unpressed.png')), 0.1)
exit_button = Button(scr_width // 2 - 103, scr_height // 2 + 100,
                     (pygame.image.load('graphics/Tileset/Buttons/Cross_Unpressed.png')), 0.1)
# Exit conditions
menu = True
gameover = False
keys = pygame.key.get_pressed()

while not gameover:

    clock.tick(clock_speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                game_state = 1

    while menu:
        i = 0
        while i < scroll_math:
            for x in range(0, 6):
                screen.blit(bg_images[x], (bg_images[x].get_width() * i + scroll[x], 0))
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = True
                    menu = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        menu = False

        for x in range(0, 6):
            scroll[x] -= 0.1 * x

        for x in range(0, 6):
            if abs(scroll[x]) > bg_images[x].get_width():
                scroll[x] = 0

        if exit_button.draw():
            gameover = True
            menu = False
        if start_button.draw():
            menu = False

        draw_text('Dungeon Depths', font_3, white, scr_width // 2 - 230, 45)
        pygame.display.flip()

    if not menu and not gameover:

        # screen.blit(background_1, (0,0))
        # screen.blit(background_pillar, (0,0))

        world.draw()
        #draw_grid()
        if game_state == 0:
            totalCoins = len(coinGroup)
            enemyGroup.update()
            # update score
            if pygame.sprite.spritecollide(player, coinGroup, True):
                score += 1
                coin_sound.play()
            if pygame.sprite.spritecollide(player, exitGroup, False):
                if totalCoins == 0:
                    game_state = 1
                else:
                    pass
            draw_text(str(score) + '/' + str(totalCoins + score), font_2, white, exitListX[0] + (tile_size // 6), exitListY[0] - (tile_size // 2))
            if level == 0:
                draw_text('This is the player', font_2, white, scr_width // 15, scr_height - 140)
                draw_text('Use A+D or the', font_2, white, scr_width // 15, scr_height - 120)
                draw_text('Arrow keys to move', font_2, white, scr_width // 15, scr_height - 100)
                draw_text('Press space to jump!', font_2, white, scr_width // 2.55, scr_height - 130)
                draw_text('Collect coins', font_2, white, scr_width // 1.49, scr_height - 110)
                draw_text('Reach the exit', font_2, white, scr_width - 175, scr_height - 165)
                draw_text('to move on!', font_2, white, scr_width - 175, scr_height - 145)
            elif level == 1:
                draw_text('This is a spike', font_2, white, scr_width // 2 - 85, scr_height // 1.3)
                draw_text('It will kill you :)', font_2, white, scr_width // 2 - 90, scr_height // 1.25)
            elif level == 2:
                draw_text('Try jump over these spikes!', font_2, white, scr_width // 2 - 150, scr_height // 1.4)
            elif level == 3:
                draw_text('This is an enemy', font_2, white, scr_width // 2 - 85, scr_height // 1.3)
                draw_text('It will also kill you', font_2, white, scr_width // 2 - 95, scr_height // 1.25)
            elif level == 4:
                draw_text('Try this!', font_1, white, scr_width // 2 - 100, scr_height // 2)
        enemyGroup.draw(screen)
        spikeGroup.draw(screen)
        coinGroup.draw(screen)
        exitGroup.draw(screen)
        draw_grid()
        game_state = player.update(game_state)

        if game_state == -1:
            if restart_button.draw():
                player.reset(98, (scr_height - 180))
                game_state = 0

        # if player has finished level
        if game_state == 1:
            level += 1
            if level <= max_levels:
                # reset level
                world_data = []
                world = reset_level(level)
                game_state = 0
                score = 0
            else:
                # restart game
                if restart_button.draw():
                    level = 0
                    world_data = []
                    world = reset_level(level)
                    game_state = 0

        pygame.display.flip()
        screen.fill(black)

pygame.quit()
