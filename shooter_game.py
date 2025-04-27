import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Min Shooter Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 20
player_speed = 5

# Bullets
bullets = []
bullet_speed = 7
bullet_size = 5

# Enemies
enemies = []
enemy_size = 40
enemy_speed = 2
enemy_spawn_rate = 30

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Game loop
clock = pygame.time.Clock()

def draw_player(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, player_size, player_size))

def draw_bullet(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, bullet_size, bullet_size))

def draw_enemy(x, y):
    pygame.draw.rect(screen, RED, (x, y, enemy_size, enemy_size))

def show_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def game_over():
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 18))
    pygame.display.update()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append([player_x + player_size // 2 - bullet_size // 2, player_y])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed

    # Spawn enemies
    if random.randint(1, enemy_spawn_rate) == 1:
        enemies.append([random.randint(0, WIDTH - enemy_size), -enemy_size])

    # Move bullets
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Move enemies
    for enemy in enemies[:]:
        enemy[1] += enemy_speed
        if enemy[1] > HEIGHT:
            enemies.remove(enemy)
            game_over()

    # Check collisions
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if (bullet[0] < enemy[0] + enemy_size and
                bullet[0] + bullet_size > enemy[0] and
                bullet[1] < enemy[1] + enemy_size and
                bullet[1] + bullet_size > enemy[1]):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                break

    # Draw everything
    draw_player(player_x, player_y)
    for bullet in bullets:
        draw_bullet(bullet[0], bullet[1])
    for enemy in enemies:
        draw_enemy(enemy[0], enemy[1])
    show_score()

    pygame.display.update()
    clock.tick(60)

pygame.quit()