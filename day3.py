import pygame
import random
import sys

# --- Initialization and Setup ---
print('Loading pygame...')
pygame.init()
print('Pygame Loaded')
print('')
print('Loading game files...')
print('')
# Screen settings
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Shooter (v0.1) (720p (1080x720) @ 60 FPS)")
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
bullet_width, bullet_height = 5, 10
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
HIGHSCORE_FILE = 'highscore.txt'
print('found highscore.txt')
print('loaded High Score')
print('')
print('')
print('Game files loaded')
print('')
print('')
print('How to Play')
print(' To move player right press: D or Right Arrow')
print(' To move player left press: A or Left Arrow')
print(' To shoot press: W, Space or Up Arrow')

# --- Functions ---
def load_high_score():
    """Load high score from file."""
    try:
        with open(HIGHSCORE_FILE, 'r') as file:
            return int(file.read())
    except (IOError, ValueError):
        return 0

def save_high_score(new_score):
    """Save high score to file."""
    with open(HIGHSCORE_FILE, 'w') as file:
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

# Initialize mixer and load sound
pygame.mixer.init()
try:
    sound1 = pygame.mixer.Sound("audio/gunshot.mp3")
except pygame.error:
    print("Failed to load sound file 'gunshot.mp3'. Make sure the file exists in the 'audio' folder.")
    sound1 = None  # Set to None to prevent errors later

try:
    sound2 = pygame.mixer.Sound("audio/die.wav")
except pygame.error:
    print("Failed to load sound file 'die.wav'. Make sure the file exists in the 'audio' folder.")
    sound2 = None  # Set to None to prevent errors later

try:
    sound3 = pygame.mixer.Sound("audio/fail.wav")
except pygame.error:
    print("Failed to load sound file 'die.wav'. Make sure the file exists in the 'audio' folder.")
    sound3 = None  # Set to None to prevent errors later

# --- Game Loop ---
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Shoot a bullet on key down
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_SPACE, pygame.K_w]:
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

    # Draw player, bullets, enemies
    pygame.draw.rect(screen, BLUE, player)
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 120, 10))
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, 10))

    pygame.display.flip()

# --- Game Over Screen ---
screen.fill(BLACK)

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