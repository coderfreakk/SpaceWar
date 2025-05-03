import pygame
import random
import math

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Shooter")

# Load assets
player_img = pygame.image.load("player.png")
alien_img = pygame.image.load("alien.png")
bullet_img = pygame.image.load("bullet.png")
background_img = pygame.image.load("background.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Sounds
pygame.mixer.music.load("background_music.ogg")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)  # Initial volume: 0.2
shoot_sound = pygame.mixer.Sound("shoot.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")

# Resize images
player_img = pygame.transform.scale(player_img, (80, 90))
alien_img = pygame.transform.scale(alien_img, (60, 50))
bullet_img = pygame.transform.scale(bullet_img, (10, 20))

# Fonts
font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 72)

# Game variables
player_x = WIDTH // 2
player_y = HEIGHT - 70
player_speed = 5

bullet_x = 0
bullet_y = player_y
bullet_speed = 7
bullet_state = "ready"

score = 0
target_score = 30

game_state = "menu"  

# Difficulty settings default
difficulty = "Medium"
num_enemies = 6
enemy_speed = 3
enemy_x, enemy_y, enemy_speed_x, enemy_speed_y = [], [], [], []

# Music volume (0.0 to 1.0)
music_volume = 0.2

def create_enemies(num, speed):
    ex, ey, esx, esy = [], [], [], []
    for _ in range(num):
        ex.append(random.randint(0, WIDTH - 64))
        ey.append(random.randint(50, 150))
        esx.append(speed)
        esy.append(40)
    return ex, ey, esx, esy

def player(x, y):
    screen.blit(player_img, (x, y))

def alien(x, y):
    screen.blit(alien_img, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    shoot_sound.play()
    screen.blit(bullet_img, (x + 16, y))

def is_collision(ex, ey, bx, by):
    return math.hypot(ex - bx, ey - by) < 27

def show_score():
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

def draw_text_center(text, size, y, color=(255, 255, 255)):
    font_obj = pygame.font.SysFont(None, size)
    text_surface = font_obj.render(text, True, color)
    rect = text_surface.get_rect(center=(WIDTH // 2, y))
    screen.blit(text_surface, rect)

def show_info():
    draw_text_center("Game Controls", 48, 80)
    draw_text_center("Left Arrow  - Move Left", 32, 140)
    draw_text_center("Right Arrow - Move Right", 32, 180)
    draw_text_center("Space       - Shoot", 32, 220)
    draw_text_center("1           - Set Easy Difficulty", 32, 260)
    draw_text_center("2           - Set Medium Difficulty", 32, 300)
    draw_text_center("3           - Set Hard Difficulty", 32, 340)
    draw_text_center("Up Arrow    - Increase Music Volume", 32, 380)
    draw_text_center("Down Arrow  - Decrease Music Volume", 32, 420)
    draw_text_center("ESC         - Back to Menu / Exit", 32, 460)

def show_volume():
    vol_percent = int(music_volume * 100)
    text = font.render(f"Music Volume: {vol_percent}%", True, (255, 255, 255))
    screen.blit(text, (WIDTH - 220, 10))

clock = pygame.time.Clock()
running = True

while running:
    screen.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if game_state == "menu":
        draw_text_center("Alien Shooter", 72, 150)
        draw_text_center("1: Easy  2: Medium  3: Hard", 36, 250)
        draw_text_center(f"Selected Difficulty: {difficulty}", 36, 290)
        draw_text_center("Up/Down Arrows: Adjust Music Volume", 32, 330)
        draw_text_center(f"Music Volume: {int(music_volume * 100)}%", 28, 370)
        draw_text_center("Press SPACE to Start", 36, 420)
        draw_text_center("Press I for Info", 36, 460)
        draw_text_center("Press ESC to Exit", 36, 500)

        # Difficulty select
        if keys[pygame.K_1]:
            difficulty = "Easy"
            num_enemies, enemy_speed = 4, 2
        elif keys[pygame.K_2]:
            difficulty = "Medium"
            num_enemies, enemy_speed = 6, 3
        elif keys[pygame.K_3]:
            difficulty = "Hard"
            num_enemies, enemy_speed = 8, 4

        # Adjust music volume
        if keys[pygame.K_UP]:
            music_volume = min(1.0, music_volume + 0.01)
            pygame.mixer.music.set_volume(music_volume)
        elif keys[pygame.K_DOWN]:
            music_volume = max(0.0, music_volume - 0.01)
            pygame.mixer.music.set_volume(music_volume)

        # Start game
        if keys[pygame.K_SPACE]:
            score = 0
            enemy_x, enemy_y, enemy_speed_x, enemy_speed_y = create_enemies(num_enemies, enemy_speed)
            bullet_state = "ready"
            bullet_y = player_y
            player_x = WIDTH // 2
            game_state = "playing"

        # Info screen
        if keys[pygame.K_i]:
            game_state = "info"

        # Exit game
        if keys[pygame.K_ESCAPE]:
            running = False

    elif game_state == "info":
        show_info()
        draw_text_center("Press ESC to return to Menu", 28, HEIGHT - 50)

        if keys[pygame.K_ESCAPE]:
            game_state = "menu"

    elif game_state == "playing":
        # Player movement
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        player_x = max(0, min(WIDTH - 64, player_x))

        # Bullet movement
        if keys[pygame.K_SPACE] and bullet_state == "ready":
            bullet_x = player_x
            fire_bullet(bullet_x, bullet_y)

        if bullet_state == "fire":
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_speed
        if bullet_y <= 0:
            bullet_y = player_y
            bullet_state = "ready"

        # Enemies
        for i in range(num_enemies):
            enemy_x[i] += enemy_speed_x[i]
            if enemy_x[i] <= 0 or enemy_x[i] >= WIDTH - 64:
                enemy_speed_x[i] *= -1
                enemy_y[i] += enemy_speed_y[i]

            if enemy_y[i] > HEIGHT - 100:
                game_state = "gameover"
                break

            if is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
                explosion_sound.play()
                bullet_y = player_y
                bullet_state = "ready"
                score += 1
                enemy_x[i] = random.randint(0, WIDTH - 64)
                enemy_y[i] = random.randint(50, 150)

            alien(enemy_x[i], enemy_y[i])

        if score >= target_score:
            game_state = "win"

        player(player_x, player_y)
        show_score()
        show_volume()

    elif game_state == "gameover":
        draw_text_center("GAME OVER", 72, 200)
        draw_text_center("Press R to Restart or ESC to Quit", 36, 300)
        if keys[pygame.K_r]:
            game_state = "menu"
        elif keys[pygame.K_ESCAPE]:
            running = False

    elif game_state == "win":
        draw_text_center("YOU WIN!", 72, 200)
        draw_text_center("Press R to Restart or ESC to Quit", 36, 300)
        if keys[pygame.K_r]:
            game_state = "menu"
        elif keys[pygame.K_ESCAPE]:
            running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
