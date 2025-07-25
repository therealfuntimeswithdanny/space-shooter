import pygame
import random
import sys
import os # <--- ADD THIS LINE

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

# --- Initialization and Setup ---
# ... (rest of your existing code) ...

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
pygame.display.set_caption("Space Shooter (v0.2)")
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
enemy_speed = 1
enemies_allowed = 5
score = 0
lives = 3
high_score = 0  # Initialize high score
print('')
print('loading High Score from highscore.txt')
# High score file name
HIGHSCORE_FILE = 'highscore.txt' # This path will be handled by resource_path for loading
# We'll put the highscore.txt in the root of the bundled app's resources for simplicity
# So the add-data will be: --add-data "highscore.txt:."
print('found highscore.txt') # This print is a bit misleading, it just finds the name
print('loaded High Score') # This print is also misleading, it's about to be loaded
print('')

# --- Load Player Image ---
try:
    # Use resource_path for the image
    player_image = pygame.image.load(resource_path('assets/player_ship.png')).convert_alpha()
    player_image = pygame.transform.scale(player_image, (player_width, player_height))
    print("Player image 'player_ship.png' loaded successfully.")
except pygame.error as e:
    print(f"Error loading player image: {e}")
    print("Falling back to drawing a blue rectangle for the player.")
    player_image = None

try:
    # Use resource_path for the bullet image
    bullet_image = pygame.image.load(resource_path('assets/bullet.png')).convert_alpha()
    bullet_image = pygame.transform.scale(bullet_image, (bullet_width, bullet_height))
    print("Bullet image 'bullet.png' loaded successfully.")
except pygame.error as e:
    print(f"Error loading bullet image: {e}")
    print("Falling back to drawing a white rectangle for bullets.")
    bullet_image = None

try:
    # Use resource_path for the enemy image
    enemy_image = pygame.image.load(resource_path('assets/enemy.png')).convert_alpha()
    enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))
    enemy_image = pygame.transform.flip(enemy_image, False, True)
    print("Enemy image 'enemy.png' loaded successfully.") # Typo in original print: "eneny.png"
except pygame.error as e:
    print(f"Error loading enemy image: {e}") # Corrected print for clarity
    print("Falling back to drawing a red rectangle for enemies.") # Corrected fallback description
    enemy_image = None # Set to None for enemy image fallback

# --- Functions ---
def load_high_score():
    """Load high score from file."""
    try:
        # Use resource_path for the highscore file
        with open(resource_path(HIGHSCORE_FILE), 'r') as file:
            return int(file.read())
    except (IOError, ValueError):
        return 0

def save_high_score(new_score):
    """Save high score to file."""
    # Use resource_path for the highscore file
    with open(resource_path(HIGHSCORE_FILE), 'w') as file:
        file.write(str(new_score))

def spawn_enemy():
    """Create a new enemy and add it to the enemies list."""
    x = random.randint(0, WIDTH - enemy_width)
    y = random.randint(-150, -40)
    enemy = pygame.Rect(x, y, enemy_width, enemy_height)
    enemies.append(enemy)

# --- Main Game Setup ---
high_score = load_high_score()  # Load the high score at the start of the game
player = pygame.Rect(WIDTH // 2 - player_width // 2, HEIGHT - 60, player_width, player_height)
player_speed = 5
bullets = []
enemies = []

# Spawn initial enemies
for _ in range(enemies_allowed):
    spawn_enemy()

print('loading audio files...')
#background music
print('')
print('loading background music...')
try:
    # Use resource_path for music
    pygame.mixer.music.load(resource_path("audio/music.mp3"))
    print("Background music 'music.mp3' loaded.")
    print('loaded background music')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"Failed to load or play background music: {e}")
print('')
print('loading sound effects...')
# No need for the 'backmusic' variable if it's not used. Removed.
# Re-initializing mixer here is redundant if it's already done at the top. Removed.
try:
    # Use resource_path for sound1
    sound1 = pygame.mixer.Sound(resource_path("audio/gunshot.mp3"))
    print('loaded gunshot.mp3')
except pygame.error as e: # Added 'as e' for specific error message
    print(f"Failed to load sound file 'gunshot.mp3': {e}. Make sure the file exists in the 'audio' folder.")
    sound1 = None

try:
    # Use resource_path for sound2
    sound2 = pygame.mixer.Sound(resource_path("audio/die.wav"))
    print('loaded die.wav')
except pygame.error as e:
    print(f"Failed to load sound file 'die.wav': {e}. Make sure the file exists in the 'audio' folder.")
    sound2 = None

try:
    # Use resource_path for sound3
    sound3 = pygame.mixer.Sound(resource_path("audio/fail.wav"))
    print('loaded fail.wav')
except pygame.error as e:
    print(f"Failed to load sound file 'fail.wav': {e}. Make sure the file exists in the 'audio' folder.")
    sound3 = None

try:
    # Use resource_path for sound4
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
# --- Game Loop ---
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Shoot a bullet on key down or mouse click
        if event.type == pygame.MOUSEBUTTONDOWN or \
           (event.type == pygame.KEYDOWN and event.key in [pygame.K_UP, pygame.K_SPACE, pygame.K_w]):
            if len(bullets) < bullets_allowed:
                bullet = pygame.Rect(player.centerx - bullet_width // 2, player.top, bullet_width, bullet_height)
                bullets.append(bullet)
                if sound1: # Only play if the sound was loaded successfully
                    sound1.play()

    # Player movement (held keys)
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.left > 0:
        player.x -= player_speed
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.right < WIDTH:
        player.x += player_speed

    # Check for the 'r' key to quit
    if keys[pygame.K_r]:
        print('game forced quit by "R" key')
        print('')
        running = False # Exit the game loop

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
            spawn_enemy()
            lives -= 1
            if sound4:
               sound4.play()
            if lives <= 0:
                running = False

    # Bullet-enemy collision
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                spawn_enemy()
                score += 1
                if sound2: # Only play if the sound was loaded successfully
                    sound2.play()
                break

    # --- Draw player, bullets, enemies ---
    # Draw the player image if loaded, otherwise draw a blue rectangle
    if player_image:
        screen.blit(player_image, player)
    else:
        pygame.draw.rect(screen, BLUE, player) # Fallback to drawing a rectangle

    for bullet in bullets:
        if bullet_image: # Check if the bullet image was loaded successfully
            screen.blit(bullet_image, bullet) # Draw the bullet image
        else:
            pygame.draw.rect(screen, WHITE, bullet) # Fallback: Draw a white rectangle
    for enemy in enemies:
        if enemy_image: # Check if the enemy image was loaded successfully
            screen.blit(enemy_image, enemy) # Draw the enemy image
        else:
            pygame.draw.rect(screen, RED, enemy) # Fallback: Draw a red rectangle

    # Draw score, lives, high score, and copyright
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)

    # Corrected copyright text rendering and positioning
    copyright_text = font.render("Version 0.2", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 120, 10))
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, 10))

    # Position the copyright text in the bottom right with padding
    screen.blit(copyright_text, (WIDTH - copyright_text.get_width() - 10, HEIGHT - copyright_text.get_height() - 10))

    pygame.display.flip()

# --- Game Over Screen ---
screen.fill(BLACK)
#play sound effect for passing lvl 10

# Check for a new high score
if score > high_score:
    save_high_score(score)
    high_score = score
    new_high_score_text = font.render("NEW High Score!", True, WHITE)
    screen.blit(new_high_score_text, (WIDTH // 2 - new_high_score_text.get_width() // 2, HEIGHT // 2 - 80))
if sound3: # Only play if the sound was loaded successfully
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
# Quit
pygame.quit()
sys.exit()