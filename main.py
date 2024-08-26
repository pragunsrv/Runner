import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Runner Game - Version 6")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

player_width = 50
player_height = 60
player_x = WIDTH // 4
player_y = HEIGHT - player_height - 10
player_velocity = 5
player_jump = False
jump_height = 10
jump_count = 10
dash_velocity = 15
dashing = False
dash_cooldown = 0

obstacle_width = 50
obstacle_height = 50
obstacle_velocity = 7

score = 0
lives = 3
invincible = False
invincible_duration = 0
font = pygame.font.SysFont('comicsans', 30, True)

background_scroll_speed = 2
background_x = 0

def draw_window(obstacles, powerups, coins, lives, invincible, dashing):
    global background_x

    background_x -= background_scroll_speed
    if background_x <= -WIDTH:
        background_x = 0

    window.fill(WHITE)
    pygame.draw.rect(window, BLACK, (background_x, 0, WIDTH, HEIGHT))
    pygame.draw.rect(window, BLACK, (background_x + WIDTH, 0, WIDTH, HEIGHT))

    pygame.draw.rect(window, BLACK, (player_x, player_y, player_width, player_height))
    for obs in obstacles:
        obs.draw()
    for powerup in powerups:
        powerup.draw()
    for coin in coins:
        coin.draw()
    score_text = font.render(f'Score: {score}', 1, BLUE)
    lives_text = font.render(f'Lives: {lives}', 1, RED)
    invincible_text = font.render(f'Invincible: {invincible}', 1, GREEN if invincible else BLACK)
    dash_text = font.render(f'Dashing: {dashing}', 1, ORANGE if dashing else BLACK)
    window.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
    window.blit(lives_text, (10, 10))
    window.blit(invincible_text, (10, 50))
    window.blit(dash_text, (10, 90))
    pygame.display.update()

def handle_collision(obstacles, coins):
    global run
    global score
    global lives
    global invincible
    for obs in obstacles:
        if (player_x < obs.x < player_x + player_width or player_x < obs.x + obs.width < player_x + player_width) and \
           (player_y < obs.y < player_y + player_height or player_y < obs.y + obs.height < player_y + player_height):
            if not invincible:
                lives -= 1
                if lives <= 0:
                    run = False
            obstacles.remove(obs)
    for coin in coins:
        if (player_x < coin.x < player_x + player_width or player_x < coin.x + coin.width < player_x + player_width) and \
           (player_y < coin.y < player_y + player_height or player_y < coin.y + coin.height < player_y + player_height):
            score += 2
            coins.remove(coin)

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

class Coin:
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
    global player_jump
    global jump_count
    global score
    global lives
    global invincible
    global invincible_duration
    global dashing
    global dash_cooldown

    obstacles = [Obstacle(WIDTH, HEIGHT - obstacle_height - 10, obstacle_width, obstacle_height, obstacle_velocity, RED)]
    for _ in range(3):
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

    coins = []
    coin_width = 20
    coin_height = 20
    coin_velocity = 7

    def add_coin():
        coin_x = random.randint(WIDTH, WIDTH + 500)
        coin_y = random.randint(0, HEIGHT - coin_height - 10)
        coins.append(Coin(coin_x, coin_y, coin_width, coin_height, coin_velocity, YELLOW))

    for _ in range(4):
        add_coin()

    def add_health_powerup():
        powerup_x = random.randint(WIDTH, WIDTH + 500)
        powerup_y = random.randint(0, HEIGHT - powerup_height - 10)
        powerups.append(Obstacle(powerup_x, powerup_y, powerup_width, powerup_height, powerup_velocity, PURPLE))

    add_health_powerup()

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
        if not player_jump:
            if keys[pygame.K_UP] and player_y - player_velocity > 0:
                player_y -= player_velocity
            if keys[pygame.K_DOWN] and player_y + player_velocity < HEIGHT - player_height:
                player_y += player_velocity
            if keys[pygame.K_SPACE]:
                player_jump = True
        else:
            if jump_count >= -jump_height:
                neg = 1
                if jump_count < 0:
                    neg = -1
                player_y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                player_jump = False
                jump_count = jump_height
        
        if keys[pygame.K_LSHIFT] and not dashing and dash_cooldown == 0:
            dashing = True
            player_velocity = dash_velocity
        if dashing:
            dash_cooldown += 1
            if dash_cooldown > 20:
                dashing = False
                player_velocity = 5
                dash_cooldown = 0
        
        for obs in obstacles:
            obs.move()
        reset_obstacle(obstacles)
        handle_collision(obstacles, coins)
        
        for powerup in powerups:
            powerup.move()
            if (player_x < powerup.x < player_x + player_width or player_x < powerup.x + powerup.width < player_x + player_width) and \
               (player_y < powerup.y < player_y + player_height or player_y < powerup.y + powerup.height < player_y + player_height):
                if powerup.color == GREEN:
                    score += 5
                elif powerup.color == PURPLE:
                    lives += 1
                powerups.remove(powerup)
                if powerup.color == GREEN:
                    add_powerup()
                elif powerup.color == PURPLE:
                    add_health_powerup()

        if invincible:
            invincible_duration += 1
            if invincible_duration > 100:
                invincible = False
                invincible_duration = 0

        for coin in coins:
            coin.move()
        
        draw_window(obstacles, powerups, coins, lives, invincible, dashing)

    pygame.quit()

if __name__ == "__main__":
    main()
