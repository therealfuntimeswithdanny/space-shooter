import pygame
import random
import sys
import os
import requests

# --- ADD THIS FUNCTION START ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # For development, use the current directory
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
# --- ADD THIS FUNCTION END ---
# --- ADD THESE LINES ---
CURRENT_APP_VERSION = "1.1" # <--- IMPORTANT: MATCH THIS TO YOUR CURRENT RELEASE VERSION
# REPLACE THESE URLs with your actual GitHub links!
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/therealfuntimeswithdanny/space-shooter-game/main/version.txt"
GITHUB_RELEASES_PAGE_URL = "https://github.com/therealfuntimeswithdanny/space-shooter-game/releases"
# --- END ADD ---  
# ... (resource_path function and other initial setup) ...

def check_for_updates():
    """Checks for a new version of the game available on GitHub."""
    print("Checking for updates...")
    try:
        # Use a timeout to prevent the game from hanging if there's no internet
        response = requests.get(GITHUB_VERSION_URL, timeout=5)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        latest_version = response.text.strip()

        if latest_version != CURRENT_APP_VERSION:
            print(f"New version available! Your version: {CURRENT_APP_VERSION}, Latest: {latest_version}")
            print(f"Download the new version at: {GITHUB_RELEASES_PAGE_URL}")
            return True, latest_version # Returns (True, "1.0.0") if update needed
        else:
            print("Game is up to date.")
            return False, None # Returns (False, None) if no update needed
    except requests.exceptions.ConnectionError:
        print("Could not check for updates: No internet connection.")
        return False, None
    except requests.exceptions.Timeout:
        print("Could not check for updates: Connection timed out.")
        return False, None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while checking for updates: {e}")
        return False, None
    except Exception as e:
        print(f"An unexpected error occurred during update check: {e}")
        return False, None

# ... (rest of your game code, e.g., load_high_score, spawn_enemy functions) ...
# --- Initialization and Setup ---
print('Loading pygame...')
pygame.init()
print('Pygame Loaded')
print('')
print('loading Pygame Mixer...')
pygame.mixer.init()
print('Pygame Mixer Loaded')
print('')
print('Loading game files...')
print('')
# Screen settings
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter (v1.1)")
print('Set display size to 720p (1080x720)')

# Clock
clock = pygame.time.Clock()
FPS = 60
print('Set FPS to 60')
print('')
# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
BLACK = (0, 0, 0)
print('Set colors')

# Font
font = pygame.font.SysFont(None, 36)
print('Loaded fonts')

# --- Game Variables ---
player_width, player_height = 50, 30
bullet_speed = -8
bullet_width, bullet_height = 5, 10 # <-- This defines bullet size
bullets_allowed = 10
enemy_width, enemy_height = 40, 30
enemy1_width, enemy1_height = 40, 30
enemy_speed = 1
enemies_allowed = 2 # Initial number of enemies
enemies_allowed_lvl100 = 3 # This can remain for separate enemy type if desired
score = 0
lives = 3
high_score = 0  # Initialize high score
print('')
print('loading High Score from highscore.txt')
# High score file name
HIGHSCORE_FILE = 'highscore.txt'
print('found highscore.txt')
print('loaded High Score')
print('')

# --- ADD THIS SECTION FOR UPDATE NOTIFICATION ---
update_available, latest_version = check_for_updates()
update_message_display_time = 3000 # Milliseconds to show the message (e.g., 3 seconds)
update_message_start_time = 0

if update_available:
    update_message_start_time = pygame.time.get_ticks()
    print("Displaying update notification...")
# --- END ADD SECTION ---

# --- Load Player Image ---
try:
    player_image = pygame.image.load(resource_path('assets/player_ship.png')).convert_alpha()
    player_image = pygame.transform.scale(player_image, (player_width, player_height))
    print("Player image 'player_ship.png' loaded successfully.")
except pygame.error as e:
    print(f"Error loading player image: {e}")
    print("Falling back to drawing a blue rectangle for the player.")
    player_image = None

try:
    bullet_image = pygame.image.load(resource_path('assets/bullet.png')).convert_alpha()
    bullet_image = pygame.transform.scale(bullet_image, (bullet_width, bullet_height))
    print("Bullet image 'bullet.png' loaded successfully.")
except pygame.error as e:
    print(f"Error loading bullet image: {e}")
    print("Falling back to drawing a white rectangle for bullets.")
    bullet_image = None

try:
    enemy_image = pygame.image.load(resource_path('assets/enemy.png')).convert_alpha()
    enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))
    enemy_image = pygame.transform.flip(enemy_image, False, True)
    print("Enemy image 'enemy.png' loaded successfully.")
except pygame.error as e:
    print(f"Error loading enemy image: {e}")
    print("Falling back to drawing a red rectangle for enemies.")
    enemy_image = None
try:
    enemy1_image = pygame.image.load(resource_path('assets/enemy.png')).convert_alpha()
    enemy1_image = pygame.transform.scale(enemy1_image, (enemy1_width, enemy1_height))
    enemy1_image = pygame.transform.flip(enemy1_image, False, True)
    print("Enemy image 'enemy.png' loaded successfully.")
except pygame.error as e:
    print(f"Error loading enemy image: {e}")
    print("Falling back to drawing a red rectangle for enemies.")
    enemy1_image = None
try:
    background_image = pygame.image.load(resource_path('assets/background/bg2.png')).convert_alpha()
    print("Background image 'background.png' loaded successfully.")
except pygame.error as e:
    print(f"Error loading background image: {e}")
    print("Falling back to a black background.")
    background_image = None
# --- Functions ---
def load_high_score():
    """Load high score from file."""
    try:
        with open(resource_path(HIGHSCORE_FILE), 'r') as file:
            return int(file.read())
    except (IOError, ValueError):
        return 0

def save_high_score(new_score):
    """Save high score to file."""
    with open(resource_path(HIGHSCORE_FILE), 'w') as file:
        file.write(str(new_score))

def spawn_enemy():
    """Create a new enemy and add it to the enemies list."""
    x = random.randint(0, WIDTH - enemy_width)
    y = random.randint(-150, -40)
    enemy = pygame.Rect(x, y, enemy_width, enemy_height)
    enemies.append(enemy)

def spawn_enemy1():
    """Create a new enemy and add it to the enemies list."""
    x = random.randint(0, WIDTH - enemy1_width)
    y = random.randint(-150, -40)
    enemy1 = pygame.Rect(x, y, enemy1_width, enemy1_height)
    enemies.append(enemy1)

# --- Main Game Setup ---
high_score = load_high_score()
player = pygame.Rect(WIDTH // 2 - player_width // 2, HEIGHT - 60, player_width, player_height)
player_speed = 5
bullets = []
enemies = []

# --- Initial enemy spawn based on enemies_allowed ---
for _ in range(enemies_allowed):
    spawn_enemy()

for _ in range(enemies_allowed_lvl100):
    spawn_enemy1()
print('loading audio files...')
#background music
print('')
print('loading background music...')
try:
    pygame.mixer.music.load(resource_path("audio/music.mp3"))
    print("Background music 'music.mp3' loaded.")
    print('loaded background music')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"Failed to load or play background music: {e}")
print('')
print('loading sound effects...')
try:
    sound1 = pygame.mixer.Sound(resource_path("audio/gunshot.mp3"))
    print('loaded gunshot.mp3')
except pygame.error as e:
    print(f"Failed to load sound file 'gunshot.mp3': {e}. Make sure the file exists in the 'audio' folder.")
    sound1 = None

try:
    sound2 = pygame.mixer.Sound(resource_path("audio/die.wav"))
    print('loaded die.wav')
except pygame.error as e:
    print(f"Failed to load sound file 'die.wav': {e}. Make sure the file exists in the 'audio' folder.")
    sound2 = None

try:
    sound3 = pygame.mixer.Sound(resource_path("audio/fail.wav"))
    print('loaded fail.wav')
except pygame.error as e:
    print(f"Failed to load sound file 'fail.wav': {e}. Make sure the file exists in the 'audio' folder.")
    sound3 = None

try:
    sound4 = pygame.mixer.Sound(resource_path("audio/life.wav"))
    print('loaded life.wav')
except pygame.error as e:
    print(f"Failed to load sound file 'life.wav': {e}. Make sure the file exists in the 'audio' folder.")
    sound4 = None


print('all audio files loaded')
print('')
print('Game files loaded')
print('')
print('')
print('How to Play')
print(' To move player right press: D or Right Arrow')
print(' To move player left press: A or Left Arrow')
print(' To shoot press: W, Space or Up Arrow')

# --- New variable to track score thresholds for enemy increases ---
next_enemy_increase_score = 20 # Score at which the next enemy will be added

# --- Game Loop ---
running = True
while running:
    clock.tick(FPS)

    # ... (inside your while running: loop) ...

# Player movement (held keys)
# ... (existing player movement and bullet/enemy logic) ...

# --- ADD THIS TO YOUR DRAWING SECTION, BEFORE pygame.display.flip() ---
    if update_available and (pygame.time.get_ticks() - update_message_start_time) < update_message_display_time:
        update_text_line1 = font.render("NEW VERSION AVAILABLE!", True, (255, 255, 0)) # Yellow text
        update_text_line2 = font.render(f"Download {latest_version} from GitHub!", True, (255, 255, 0))

        screen.blit(update_text_line1, (WIDTH // 2 - update_text_line1.get_width() // 2, HEIGHT // 2 - 80))
        screen.blit(update_text_line2, (WIDTH // 2 - update_text_line2.get_width() // 2, HEIGHT // 2 - 40))
    # --- END ADD ---

    pygame.display.flip()

    # ... (rest of your game loop) ...

    if background_image:
        bg_width = background_image.get_width()
        bg_height = background_image.get_height()
        for x in range(0, WIDTH + bg_width, bg_width):
            for y in range(0, HEIGHT + bg_height, bg_height):
                screen.blit(background_image, (x, y))
    else:
        screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN or \
           (event.type == pygame.KEYDOWN and event.key in [pygame.K_UP, pygame.K_SPACE, pygame.K_w]):
            if len(bullets) < bullets_allowed:
                bullet = pygame.Rect(player.centerx - bullet_width // 2, player.top, bullet_width, bullet_height)
                bullets.append(bullet)
                if sound1:
                    sound1.play()

    # Player movement (held keys)
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.left > 0:
        player.x -= player_speed
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.right < WIDTH:
        player.x += player_speed

    if keys[pygame.K_r]:
        print('game forced quit by "R" key')
        print('')
        running = False

    # Move bullets
    for bullet in bullets[:]:
        bullet.y += bullet_speed
        if bullet.bottom < 0:
            bullets.remove(bullet)

    # Move enemies
    for enemy in enemies[:]:
        enemy.y += enemy_speed
        if enemy.top > HEIGHT:
            enemies.remove(enemy)
            spawn_enemy() # This still spawns one enemy when one goes off-screen
            lives -= 1
            if sound4:
               sound4.play()
            if lives <= 0:
                running = False
            
    # --- New logic for incrementally increasing enemy count ---
    if score >= next_enemy_increase_score:
        enemies_allowed += 1 # Increase the *total* allowed enemies by 1
        spawn_enemy() # Spawn one more enemy immediately
        next_enemy_increase_score += 5 # Set the next score threshold

    # Bullet-enemy collision
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                spawn_enemy() # This respawns the one that was hit
                score += 1
                if sound2:
                    sound2.play()
                break

    # --- Draw player, bullets, enemies ---
    if player_image:
        screen.blit(player_image, player)
    else:
        pygame.draw.rect(screen, BLUE, player)

    for bullet in bullets:
        if bullet_image:
            screen.blit(bullet_image, bullet)
        else:
            pygame.draw.rect(screen, WHITE, bullet)
    for enemy in enemies:
        if enemy_image:
            screen.blit(enemy_image, enemy)
        else:
            pygame.draw.rect(screen, RED, enemy)

    # Draw score, lives, high score, and copyright
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)

    copyright_text = font.render("Version 1", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 120, 10))
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, 10))

    screen.blit(copyright_text, (WIDTH - copyright_text.get_width() - 10, HEIGHT - copyright_text.get_height() - 10))

    pygame.display.flip()

# --- Game Over Screen ---
screen.fill(BLACK)

if score > high_score:
    save_high_score(score)
    high_score = score
    new_high_score_text = font.render("NEW High Score!", True, WHITE)
    screen.blit(new_high_score_text, (WIDTH // 2 - new_high_score_text.get_width() // 2, HEIGHT // 2 - 80))
if sound3:
    sound3.play()
game_over_text = font.render("Game Over!", True, RED)
final_score_text = font.render(f"Final Score: {score}", True, WHITE)
final_high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
game_close_text = font.render("Game will close in 5 seconds", True, RED)

screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 40))
screen.blit(game_close_text, (WIDTH // 2.5 - game_over_text.get_width() // 2, HEIGHT // 2 + 100))
screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))
screen.blit(final_high_score_text, (WIDTH // 2 - final_high_score_text.get_width() // 2, HEIGHT // 2 + 40))

pygame.display.flip()
pygame.time.wait(5000)
pygame.quit()
sys.exit()