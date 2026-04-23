import pygame
import random
import math
from pygame import mixer

# Initialize Pygame and Mixer for Sound
pygame.init()
mixer.init()

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# To use background/sounds, replace filenames with your local paths
# background = pygame.image.load('background.png') 
# mixer.music.load('background_music.wav')
# mixer.music.play(-1) # Loop forever

# Player Setup
player_img = pygame.Surface((50, 50)) # Placeholder
player_img.fill((0, 255, 0))
player_x = 370
player_y = 480
player_x_change = 0

# Enemy Setup
enemy_img = pygame.Surface((40, 40)) # Placeholder
enemy_img.fill((255, 0, 0))
num_enemies = 6
enemies = []
for i in range(num_enemies):
    enemies.append([random.randint(0, 736), random.randint(50, 150), 4, 40])

# Bullet Setup
bullet_img = pygame.Surface((10, 20)) # Placeholder
bullet_img.fill((255, 255, 0))
bullet_x = 0
bullet_y = 480
bullet_state = "ready" # "ready" = hidden, "fire" = moving

score = 0
font = pygame.font.SysFont("Arial", 32)

def show_score():
    score_render = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_render, (10, 10))

def is_collision(ex, ey, bx, by):
    distance = math.sqrt(math.pow(ex - bx, 2) + math.pow(ey - by, 2))
    return distance < 27

# Main Game Loop
running = True
while running:
    screen.fill((0, 0, 0)) # Fill black or blit background image
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: player_x_change = -5
            if event.key == pygame.K_RIGHT: player_x_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                # bullet_sound = mixer.Sound('laser.wav')
                # bullet_sound.play()
                bullet_x = player_x
                bullet_state = "fire"
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]: player_x_change = 0

    # Player Movement
    player_x += player_x_change
    player_x = max(0, min(player_x, 750))
    screen.blit(player_img, (player_x, player_y))

    # Enemy Logic
    for e in enemies:
        e[0] += e[2]
        if e[0] <= 0 or e[0] >= 760:
            e[2] *= -1
            e[1] += e[3]
        
        # Collision Check
        if is_collision(e[0], e[1], bullet_x, bullet_y):
            # explosion_sound = mixer.Sound('explosion.wav')
            # explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score += 1
            e[0], e[1] = random.randint(0, 736), random.randint(50, 150)
            
        screen.blit(enemy_img, (e[0], e[1]))

    # Bullet Movement
    if bullet_state == "fire":
        screen.blit(bullet_img, (bullet_x + 20, bullet_y))
        bullet_y -= 10
        if bullet_y <= 0:
            bullet_y = 480
            bullet_state = "ready"

    show_score()
    pygame.display.update()

pygame.quit()
