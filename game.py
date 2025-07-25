import pygame
import random
import sys
import os
import requests
import webbrowser # Import the webbrowser module

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
CURRENT_APP_VERSION = "1.2" # <--- IMPORTANT: MATCH THIS TO YOUR CURRENT RELEASE VERSION
# REPLACE THESE URLs with your actual GitHub links!
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/therealfuntimeswithdanny/space-shooter/main/version.txt"
GITHUB_RELEASES_PAGE_URL = "https://github.com/therealfuntimeswithdanny/space-shooter/releases"
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
pygame.display.set_caption("Space Shooter v1.2.1")
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
YELLOW = (255, 255, 0) # Define YELLOW color
GREEN = (0, 255, 0) # Define GREEN for bounty enemy
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
bounty_enemy_width, bounty_enemy_height = 50, 40 # Slightly larger for distinctiveness
enemy_speed = 1
bounty_enemy_speed = 2 # Bounty enemy might move at a different speed
enemies_allowed = 2 # Initial number of regular enemies
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

# --- NEW: Load Bounty Enemy Image ---
try:
    # Assuming you might want a different image, or reuse and re-color
    bounty_enemy_image = pygame.image.load(resource_path('assets/background/space-ship.gif')).convert_alpha() # Using same image for now
    bounty_enemy_image = pygame.transform.scale(bounty_enemy_image, (bounty_enemy_width, bounty_enemy_height))
    bounty_enemy_image = pygame.transform.flip(bounty_enemy_image, False, True)
    # You might want to apply a color tint or load a completely different image for distinction
    # For example, to tint:
    # bounty_enemy_image.fill((0, 255, 0, 255), special_flags=pygame.BLEND_RGBA_MULT) # Tints green
    print("Bounty enemy image 'gspace-ship.gif loaded successfully (can be visually distinct).")
except pygame.error as e:
    print(f"Error loading bounty enemy image: {e}")
    print("Falling back to drawing a green rectangle for bounty enemies.")
    bounty_enemy_image = None

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
    """Create a new regular enemy and add it to the enemies list."""
    x = random.randint(0, WIDTH - enemy_width)
    y = random.randint(-150, -40)
    # Store enemy as a dictionary to differentiate types if needed, or use separate lists
    enemy_rect = pygame.Rect(x, y, enemy_width, enemy_height)
    enemies.append({'rect': enemy_rect, 'type': 'regular'})

# --- NEW: Function to spawn a Bounty Enemy ---
def spawn_bounty_enemy():
    """Create a new bounty enemy and add it to the enemies list."""
    x = random.randint(0, WIDTH - bounty_enemy_width)
    y = random.randint(-150, -40)
    bounty_enemy_rect = pygame.Rect(x, y, bounty_enemy_width, bounty_enemy_height)
    enemies.append({'rect': bounty_enemy_rect, 'type': 'bounty'})

# --- Main Game Setup ---
high_score = load_high_score()
player = pygame.Rect(WIDTH // 2 - player_width // 2, HEIGHT - 60, player_width, player_height)
player_speed = 5
bullets = []
enemies = [] # This list will now hold dictionaries: {'rect': rect_obj, 'type': 'regular'/'bounty'}

# --- Initial enemy spawn based on enemies_allowed ---
for _ in range(enemies_allowed):
    spawn_enemy()

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

# --- NEW: Sound for bounty enemy hit ---
try:
    sound_bounty_hit = pygame.mixer.Sound(resource_path("audio/powerup.wav")) # Assuming you have a powerup sound
    print('loaded powerup.wav for bounty enemy hit.')
except pygame.error as e:
    print(f"Failed to load sound file 'powerup.wav': {e}. Make sure the file exists in the 'audio' folder.")
    sound_bounty_hit = None


print('all audio files loaded')
print('')
print('Game files loaded')
print('')
print('')
print('How to Play')
print(' To move player right press: D or Right Arrow')
print(' To move player left press: A or Left Arrow')
print(' To shoot press: W, Space or Up Arrow')
print(' To open GitHub releases page for updates: Press U') # Added instruction

# --- New variable to track score thresholds for enemy increases ---
next_enemy_increase_score = 30 # Score at which the next regular enemy will be added

# --- NEW: Bounty enemy spawn management ---
bounty_spawn_points = [
    (75, 85),
    (125, 135),
    (200, 210),
    (400, float('inf')) # Use infinity for "400+"
]
bounty_spawned_at_score = [] # To keep track of points where bounty enemy has spawned

# --- Game Loop ---
running = True
while running:
    clock.tick(FPS)

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
        
        # --- NEW: Handle 'U' key press to open GitHub page ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                print(f"Opening GitHub releases page: {GITHUB_RELEASES_PAGE_URL}")
                webbrowser.open_new_tab(GITHUB_RELEASES_PAGE_URL)
        # --- END NEW ---

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
    for enemy_data in enemies[:]:
        enemy_rect = enemy_data['rect']
        enemy_type = enemy_data['type']

        if enemy_type == 'regular':
            enemy_rect.y += enemy_speed
            if enemy_rect.top > HEIGHT:
                enemies.remove(enemy_data)
                spawn_enemy() # Respawn regular enemy if it goes off-screen
                lives -= 1
                if sound4:
                   sound4.play()
                if lives <= 0:
                    running = False
        elif enemy_type == 'bounty':
            enemy_rect.y += bounty_enemy_speed # Use bounty specific speed
            if enemy_rect.top > HEIGHT:
                enemies.remove(enemy_data)
                # Bounty enemies do NOT respawn automatically when they go off-screen
                # They are tied to specific score ranges.

    # --- Logic for incrementally increasing regular enemy count ---
    # This remains separate for regular enemies
    if score >= next_enemy_increase_score:
        # Check if we are not at 400+ score and if the current enemy count is reasonable
        # This prevents an infinite increase of regular enemies if you want a cap
        current_regular_enemies = sum(1 for e in enemies if e['type'] == 'regular')
        if current_regular_enemies < 10: # Example cap for regular enemies
            spawn_enemy() # Spawn one more regular enemy immediately
            next_enemy_increase_score += 5 # Set the next score threshold for regular enemies


    # --- NEW: Bounty enemy spawning logic ---
    for start_score, end_score in bounty_spawn_points:
        if start_score <= score <= end_score:
            # Check if a bounty enemy has already spawned for this score range
            # and if there are currently no bounty enemies on screen
            if (start_score, end_score) not in bounty_spawned_at_score and \
               not any(e['type'] == 'bounty' for e in enemies):
                spawn_bounty_enemy()
                bounty_spawned_at_score.append((start_score, end_score))
                print(f"Bounty enemy spawned at score {score}!")
            break # Only try to spawn one bounty enemy at a time based on range

    # Bullet-enemy collision
    for bullet in bullets[:]:
        for enemy_data in enemies[:]:
            enemy_rect = enemy_data['rect']
            enemy_type = enemy_data['type']

            if bullet.colliderect(enemy_rect):
                bullets.remove(bullet)
                enemies.remove(enemy_data) # Remove the hit enemy

                if enemy_type == 'regular':
                    spawn_enemy() # Respawn regular enemy
                    score += 1
                    if sound2:
                        sound2.play()
                elif enemy_type == 'bounty':
                    score += 20 # Score goes up by 20
                    lives += 2 # Gain 2 extra lives
                    if sound_bounty_hit: # Play a distinct sound for bounty enemy
                        sound_bounty_hit.play()
                    print(f"Bounty enemy defeated! Score +20, Lives +2. Current Lives: {lives}")
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
            
    for enemy_data in enemies:
        enemy_rect = enemy_data['rect']
        enemy_type = enemy_data['type']
        
        if enemy_type == 'regular':
            if enemy_image:
                screen.blit(enemy_image, enemy_rect)
            else:
                pygame.draw.rect(screen, RED, enemy_rect)
        elif enemy_type == 'bounty':
            if bounty_enemy_image:
                screen.blit(bounty_enemy_image, enemy_rect)
                # You can also draw a text overlay on bounty enemy for distinction
                bounty_text = font.render("BONUS", True, YELLOW)
                screen.blit(bounty_text, (enemy_rect.x + (bounty_enemy_width - bounty_text.get_width()) // 2, enemy_rect.y + (bounty_enemy_height - bounty_text.get_height()) // 2))
            else:
                pygame.draw.rect(screen, GREEN, enemy_rect) # Draw green if no image

    # Draw score, lives, high score
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 120, 10))
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, 10))

    # --- MODIFIED: Conditional drawing for update message or copyright ---
    if update_available:
        update_text = font.render(f"UPDATE AVAILABLE! Press 'U' to go to GitHub!", True, YELLOW)
        screen.blit(update_text, (WIDTH - update_text.get_width() - 10, HEIGHT - update_text.get_height() - 10))
    else:
        copyright_text = font.render(f"Version {CURRENT_APP_VERSION}", True, WHITE)
        screen.blit(copyright_text, (WIDTH - copyright_text.get_width() - 10, HEIGHT - copyright_text.get_height() - 10))
    # --- END MODIFIED SECTION ---

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