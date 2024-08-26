import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Runner Game - Version 12 Extended")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BROWN = (139, 69, 19)

player_width, player_height = 50, 50
player_x, player_y = 50, HEIGHT - player_height - 10
player_velocity = 10
player_jump = False
jump_count = 10
jump_height = 10
dash_velocity = 20
dash_cooldown = 50
dashing = False

obstacle_width, obstacle_height = 70, 70
obstacle_velocity = 10
max_obstacles = 5
max_coins = 3
score = 0
lives = 3
invincible = False
invincible_duration = 0
run = True
enemy_spawn_time = 0
powerup_spawn_time = 0
coin_spawn_time = 0
boss_spawned = False
difficulty_increase_rate = 0.05

background_layers = [
    pygame.image.load("layer1.png"),
    pygame.image.load("layer2.png"),
    pygame.image.load("layer3.png")
]
background_positions = [0, 0, 0]
background_speeds = [1, 2, 3]

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
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

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
        pygame.draw.circle(win, self.color, (self.x, self.y), self.width // 2)

class PowerUp:
    def __init__(self, x, y, width, height, velocity, color, type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.color = color
        self.type = type

    def move(self):
        self.x -= self.velocity

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

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
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

class FlyingEnemy(Enemy):
    def __init__(self, x, y, width, height, velocity, color):
        super().__init__(x, y, width, height, velocity, color)
        self.fly_height = random.randint(50, 150)

    def move(self):
        self.x -= self.velocity
        self.y = self.fly_height + (HEIGHT // 4) * pygame.math.sin(pygame.time.get_ticks() * 0.01)

class BossEnemy:
    def __init__(self, x, y, width, height, velocity, color, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.color = color
        self.health = health
        self.attack_pattern = random.choice([self.shoot, self.charge])

    def move(self):
        self.x -= self.velocity
        if random.randint(0, 100) < 5:
            self.attack_pattern()

    def shoot(self):
        pass

    def charge(self):
        self.velocity += 2

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def fire_projectile(self, projectiles):
        projectiles.append(Projectile(self.x, self.y + self.height // 2, 10, 10, self.velocity + 5, RED))

class Shield(PowerUp):
    pass

class ExtraLife(PowerUp):
    pass

class Projectile:
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
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

def draw_window(obstacles, powerups, coins, lives, invincible, dashing, enemies, boss, projectiles, shield, extra_life):
    win.fill(WHITE)

    for i, layer in enumerate(background_layers):
        win.blit(layer, (background_positions[i], 0))
        background_positions[i] -= background_speeds[i]
        if background_positions[i] <= -WIDTH:
            background_positions[i] = 0

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
    for projectile in projectiles:
        projectile.draw()
    if shield:
        shield.draw()
    if extra_life:
        extra_life.draw()

    pygame.draw.rect(win, BLUE if invincible else BLACK, (player_x, player_y, player_width, player_height))

    font = pygame.font.SysFont("comicsans", 30)
    lives_text = font.render(f"Lives: {lives}", 1, BLACK)
    score_text = font.render(f"Score: {score}", 1, BLACK)
    win.blit(lives_text, (10, 10))
    win.blit(score_text, (WIDTH - 150, 10))

    pygame.display.update()

def handle_collision(obstacles, coins, enemies, boss, projectiles, shield, extra_life):
    global score
    global lives
    global invincible

    for obs in obstacles:
        if (player_x < obs.x < player_x + player_width or player_x < obs.x + obs.width < player_x + player_width) and \
           (player_y < obs.y < player_y + player_height or player_y < obs.y + obs.height < player_y + player_height):
            if not invincible:
                lives -= 1
                if lives <= 0:
                    game_over()
            obstacles.remove(obs)
    for coin in coins:
        if (player_x < coin.x < player_x + player_width or player_x < coin.x + coin.width < player_x + player_width) and \
           (player_y < coin.y < player_y + player_height or player_y < coin.y + player_height < player_y + player_height):
            score += 10
            coins.remove(coin)
    for enemy in enemies:
        if (player_x < enemy.x < player_x + player_width or player_x < enemy.x + enemy.width < player_x + player_width) and \
           (player_y < enemy.y < player_y + player_height or player_y < enemy.y + player.height < player_y + player_height):
            if not invincible:
                lives -= 1
                if lives <= 0:
                    game_over()
            enemies.remove(enemy)
    if boss:
        if (player_x < boss.x < player_x + player_width or player_x < boss.x + boss.width < player_x + player_width) and \
           (player_y < boss.y < player_y + player_height or player_y < boss.y + player.height < player_y + player_height):
            if not invincible:
                lives -= 1
                if lives <= 0:
                    game_over()
            boss.health -= 1
            if boss.health <= 0:
                boss = None

def game_over():
    global run
    run = False

class BackgroundLayer:
    def __init__(self, image, speed):
        self.image = pygame.image.load(image)
        self.speed = speed
        self.x_pos = 0

    def move(self):
        self.x_pos -= self.speed
        if self.x_pos <= -WIDTH:
            self.x_pos = 0

    def draw(self):
        win.blit(self.image, (self.x_pos, 0))

class HealthBar:
    def __init__(self, max_health, x, y, width, height):
        self.max_health = max_health
        self.current_health = max_health
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        health_ratio = self.current_health / self.max_health
        pygame.draw.rect(win, RED, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(win, GREEN, (self.x, self.y, self.width * health_ratio, self.height))

    def reduce_health(self, amount):
        self.current_health -= amount
        if self.current_health < 0:
            self.current_health = 0

# Main loop
clock = pygame.time.Clock()

obstacles = []
powerups = []
coins = []
enemies = []
projectiles = []
boss = None
shield = None
extra_life = None
boss_health_bar = None

while run:
    clock.tick(30)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # Movement and jumping
    if keys[pygame.K_LEFT] and player_x - player_velocity > 0:
        player_x -= player_velocity
    if keys[pygame.K_RIGHT] and player_x + player_velocity + player_width < WIDTH:
        player_x += player_velocity
    if not player_jump:
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

    # Dashing
    if keys[pygame.K_LSHIFT] and dash_cooldown <= 0:
        dashing = True
        dash_cooldown = 50
    if dashing:
        player_x += dash_velocity
        dash_cooldown -= 1
        if dash_cooldown <= 0:
            dashing = False

    # Invincibility
    if invincible:
        invincible_duration -= 1
        if invincible_duration <= 0:
            invincible = False

    # Difficulty increase
    if score % 100 == 0 and score != 0:
        obstacle_velocity += difficulty_increase_rate
        for obs in obstacles:
            obs.velocity += difficulty_increase_rate

    # Spawn obstacles, powerups, coins, enemies, boss
    if len(obstacles) < max_obstacles:
        obstacles.append(Obstacle(WIDTH, HEIGHT - obstacle_height - 10, obstacle_width, obstacle_height, obstacle_velocity, BROWN))

    if len(coins) < max_coins and coin_spawn_time <= 0:
        coins.append(Coin(WIDTH, random.randint(50, HEIGHT - 50), 20, 20, obstacle_velocity, YELLOW))
        coin_spawn_time = 50

    if not boss and score > 500 and not boss_spawned:
        boss = BossEnemy(WIDTH - 100, HEIGHT - 200, 100, 100, 3, MAGENTA, 10)
        boss_health_bar = HealthBar(boss.health, WIDTH - 200, 10, 100, 20)
        boss_spawned = True

    # Update game elements
    handle_collision(obstacles, coins, enemies, boss, projectiles, shield, extra_life)
    draw_window(obstacles, powerups, coins, lives, invincible, dashing, enemies, boss, projectiles, shield, extra_life)

    if not run:
        break

pygame.quit()
