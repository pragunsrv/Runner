import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Runner Game - Version 2")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

player_width = 50
player_height = 60
player_x = WIDTH // 4
player_y = HEIGHT - player_height - 10
player_velocity = 5

obstacle_width = 50
obstacle_height = 50
obstacle_velocity = 7
obstacle_x = WIDTH
obstacle_y = HEIGHT - obstacle_height - 10

score = 0
font = pygame.font.SysFont('comicsans', 30, True)

def draw_window():
    window.fill(WHITE)
    pygame.draw.rect(window, BLACK, (player_x, player_y, player_width, player_height))
    pygame.draw.rect(window, RED, (obstacle_x, obstacle_y, obstacle_width, obstacle_height))
    score_text = font.render(f'Score: {score}', 1, BLUE)
    window.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
    pygame.display.update()

def handle_collision():
    global run
    global score
    if (player_x < obstacle_x < player_x + player_width or player_x < obstacle_x + obstacle_width < player_x + player_width) and \
       (player_y < obstacle_y < player_y + player_height or player_y < obstacle_y + obstacle_height < player_y + player_height):
        run = False

def reset_obstacle():
    global obstacle_x
    global obstacle_y
    global score
    if obstacle_x < 0 - obstacle_width:
        obstacle_x = WIDTH
        obstacle_y = HEIGHT - obstacle_height - 10
        score += 1

run = True
while run:
    pygame.time.delay(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x - player_velocity > 0:
        player_x -= player_velocity
    if keys[pygame.K_RIGHT] and player_x + player_velocity < WIDTH - player_width:
        player_x += player_velocity
    
    obstacle_x -= obstacle_velocity
    reset_obstacle()
    handle_collision()
    draw_window()

pygame.quit()

class Obstacle:
    def __init__(self, x, y, width, height, velocity, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.color = color

    def move(self):
        self.x -= self.velocity
        if self.x < 0 - self.width:
            self.x = WIDTH
            self.y = HEIGHT - self.height - 10

    def draw(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

def main():
    global run
    global player_x
    global player_y
    global player_velocity
    global score

    obs = Obstacle(WIDTH, HEIGHT - obstacle_height - 10, obstacle_width, obstacle_height, obstacle_velocity, RED)

    run = True
    while run:
        pygame.time.delay(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x - player_velocity > 0:
            player_x -= player_velocity
        if keys[pygame.K_RIGHT] and player_x + player_velocity < WIDTH - player_width:
            player_x += player_velocity
        
        obs.move()
        if (player_x < obs.x < player_x + player_width or player_x < obs.x + obs.width < player_x + player_width) and \
           (player_y < obs.y < player_y + player_height or player_y < obs.y + obs.height < player_y + player_height):
            run = False
        
        window.fill(WHITE)
        pygame.draw.rect(window, BLACK, (player_x, player_y, player_width, player_height))
        obs.draw()
        score_text = font.render(f'Score: {score}', 1, BLUE)
        window.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
