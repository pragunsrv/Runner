import pygame
import random

# Initialize the game
pygame.init()

# Game window dimensions
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Runner Game - Version 1")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player settings
player_width = 50
player_height = 60
player_x = WIDTH // 4
player_y = HEIGHT - player_height - 10
player_velocity = 5

# Obstacle settings
obstacle_width = 50
obstacle_height = 50
obstacle_velocity = 7
obstacle_x = WIDTH
obstacle_y = HEIGHT - obstacle_height - 10

# Game loop
run = True
while run:
    pygame.time.delay(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x - player_velocity > 0:
        player_x -= player_velocity
    if keys[pygame.K_RIGHT] and player_x + player_velocity < WIDTH - player_width:
        player_x += player_velocity
    
    # Move the obstacle
    obstacle_x -= obstacle_velocity
    if obstacle_x < 0 - obstacle_width:
        obstacle_x = WIDTH
        obstacle_y = HEIGHT - obstacle_height - 10

    # Check collision
    if (player_x < obstacle_x < player_x + player_width or player_x < obstacle_x + obstacle_width < player_x + player_width) and \
       (player_y < obstacle_y < player_y + player_height or player_y < obstacle_y + obstacle_height < player_y + player_height):
        run = False

    # Drawing everything
    window.fill(WHITE)
    pygame.draw.rect(window, BLACK, (player_x, player_y, player_width, player_height))
    pygame.draw.rect(window, BLACK, (obstacle_x, obstacle_y, obstacle_width, obstacle_height))
    pygame.display.update()

pygame.quit()
