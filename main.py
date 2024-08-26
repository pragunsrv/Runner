import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Runner Game - Version 8")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

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

enemy_width = 50
enemy_height = 60
enemies = []
enemy_spawn_time = 0
enemy_velocity = 5

# New Features
powerup_spawn_time = 0
coin_spawn_time = 0
difficulty_increase_rate = 0.01
max_obstacles = 10
max_coins = 8
boss_spawned = False

class BossEnemy:
    def __init__(self, x, y, width, height, velocity, color, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.color = color
        self.health = health

    def move(self):
        self.x -= self.velocity

    def draw(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        health_bar_length = self.width
        health_ratio = self.health / 100
        pygame.draw.rect(window, RED, (self.x, self.y - 10, health_bar_length, 5))
        pygame.draw.rect(window, GREEN, (self.x, self.y - 10, health_bar_length * health_ratio, 5))

def draw_window(obstacles, powerups, coins, lives, invincible, dashing, enemies, boss):
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
    for enemy in enemies:
        enemy.draw()
    if boss:
        boss.draw()
    score_text = font.render(f'Score: {score}', 1, BLUE)
    lives_text = font.render(f'Lives: {lives}', 1, RED)
    invincible_text = font.render(f'Invincible: {invincible}', 1, GREEN if invincible else BLACK)
    dash_text = font.render(f'Dashing: {dashing}', 1, ORANGE if dashing else BLACK)
    window.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
    window.blit(lives_text, (10, 10))
    window.blit(invincible_text, (10, 50))
    window.blit(dash_text, (10, 90))
    pygame.display.update()

def handle_collision(obstacles, coins, enemies, boss):
    global run
    global score
    global lives
    global invincible
    global boss_spawned
    if boss and (player_x < boss.x < player_x + player_width or player_x < boss.x + boss.width < player_x + player_width) and \
        (player_y < boss.y < player_y + player_height or player_y < boss.y + boss.height < player_y + player_height):
        if not invincible:
            lives -= 1
            if lives <= 0:
                run = False
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
    for enemy in enemies:
        if (player_x < enemy.x < player_x + player_width or player_x < enemy.x + enemy.width < player_x + player_width) and \
           (player_y < enemy.y < player_y + player_height or player_y < enemy.y + enemy.height < player_y + player_height):
            if not invincible:
                lives -= 1
                if lives <= 0:
                    run = False
            enemies.remove(enemy)
    if boss:
        if boss.health <= 0:
            boss_spawned = False

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

class Enemy:
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
    global enemy_spawn_time
    global powerup_spawn_time
    global coin_spawn_time
    global difficulty_increase_rate
    global max_obstacles
    global max_coins
    global boss_spawned

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

    for _ in range(max_coins):
        add_coin()

    def add_health_powerup():
        powerup_x = random.randint(WIDTH, WIDTH + 500)
        powerup_y = random.randint(0, HEIGHT - powerup_height - 10)
        powerups.append(Obstacle(powerup_x, powerup_y, powerup_width, powerup_height, powerup_velocity, PURPLE))

    add_health_powerup()

    def add_enemy():
        enemy_x = random.randint(WIDTH, WIDTH + 300)
        enemy_y = HEIGHT - enemy_height - 10
        enemies.append(Enemy(enemy_x, enemy_y, enemy_width, enemy_height, enemy_velocity, MAGENTA))

    def spawn_boss():
        return BossEnemy(WIDTH, HEIGHT - enemy_height - 10, enemy_width * 2, enemy_height * 2, enemy_velocity // 2, BLUE, 100)

    run = True
    boss = None
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
        
        if keys[pygame.K_LSHIFT] and dash_cooldown <= 0:
            dashing = True
            dash_cooldown = 50
        if dashing:
            player_x += dash_velocity
            dash_cooldown -= 1
            if dash_cooldown <= 0:
                dashing = False
                dash_cooldown = 50
        
        if invincible:
            invincible_duration -= 1
            if invincible_duration <= 0:
                invincible = False

        for obs in obstacles:
            obs.move()
        for powerup in powerups:
            powerup.move()
        for coin in coins:
            coin.move()
        for enemy in enemies:
            enemy.move()
        if boss:
            boss.move()
        
        handle_collision(obstacles, coins, enemies, boss)
        reset_obstacle(obstacles)
        
        enemy_spawn_time += 1
        if enemy_spawn_time >= 100:
            add_enemy()
            enemy_spawn_time = 0
        
        powerup_spawn_time += 1
        if powerup_spawn_time >= 150:
            add_powerup()
            powerup_spawn_time = 0
        
        coin_spawn_time += 1
        if coin_spawn_time >= 150:
            add_coin()
            coin_spawn_time = 0
        
        if not boss_spawned and score > 500:
            boss = spawn_boss()
            boss_spawned = True
        
        if boss:
            boss.health -= difficulty_increase_rate
        
        draw_window(obstacles, powerups, coins, lives, invincible, dashing, enemies, boss)
    
    pygame.quit()

if __name__ == "__main__":
    main()
