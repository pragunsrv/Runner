import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Runner Game - Version 3")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

player_width = 50
player_height = 60
player_x = WIDTH // 4
player_y = HEIGHT - player_height - 10
player_velocity = 5

obstacle_width = 50
obstacle_height = 50
obstacle_velocity = 7

score = 0
font = pygame.font.SysFont('comicsans', 30, True)

def draw_window(obstacles):
    window.fill(WHITE)
    pygame.draw.rect(window, BLACK, (player_x, player_y, player_width, player_height))
    for obs in obstacles:
        obs.draw()
    score_text = font.render(f'Score: {score}', 1, BLUE)
    window.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
    pygame.display.update()

def handle_collision(obstacles):
    global run
    for obs in obstacles:
        if (player_x < obs.x < player_x + player_width or player_x < obs.x + obs.width < player_x + player_width) and \
           (player_y < obs.y < player_y + player_height or player_y < obs.y + obs.height < player_y + player_height):
            run = False

def reset_obstacle(obstacles):
    global score
    for obs in obstacles:
        if obs.x < 0 - obs.width:
            obs.x = WIDTH
            obs.y = HEIGHT - obs.height - 10
            score += 1

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

    def draw(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

def main():
    global run
    global player_x
    global player_y
    global player_velocity
    global score

    obstacles = [Obstacle(WIDTH, HEIGHT - obstacle_height - 10, obstacle_width, obstacle_height, obstacle_velocity, RED)]
    for _ in range(2):
        obstacle_x = random.randint(WIDTH, WIDTH + 300)
        obstacle_y = HEIGHT - obstacle_height - 10
        obstacles.append(Obstacle(obstacle_x, obstacle_y, obstacle_width, obstacle_height, obstacle_velocity, RED))

    powerups = []
    powerup_width = 30
    powerup_height = 30
    powerup_velocity = 7

    def add_powerup():
        powerup_x = random.randint(WIDTH, WIDTH + 500)
        powerup_y = random.randint(0, HEIGHT - powerup_height - 10)
        powerups.append(Obstacle(powerup_x, powerup_y, powerup_width, powerup_height, powerup_velocity, GREEN))

    add_powerup()

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
        
        for obs in obstacles:
            obs.move()
        reset_obstacle(obstacles)
        handle_collision(obstacles)
        
        for powerup in powerups:
            powerup.move()
            if (player_x < powerup.x < player_x + player_width or player_x < powerup.x + powerup.width < player_x + player_width) and \
               (player_y < powerup.y < player_y + player_height or player_y < powerup.y + powerup.height < player_y + player_height):
                score += 5
                powerups.remove(powerup)
                add_powerup()
        
        draw_window(obstacles + powerups)

    pygame.quit()

if __name__ == "__main__":
    main()
