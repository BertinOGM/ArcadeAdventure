import pygame
from pygame.locals import *

# Initializing Pygame
pygame.init()

# Initializing the screen
scr_width = 1000
scr_height = 600
screen = pygame.display.set_mode((scr_width, scr_height))
pygame.display.set_caption("Platformer")

# Constants
white = (255, 255, 255)

# Setting the exit condition
game_over = False


# While loop for active game
while not game_over:
    # Main loop for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Screen clearing
    screen.fill(white)

    # Screen updating
    pygame.display.flip()

pygame.quit()