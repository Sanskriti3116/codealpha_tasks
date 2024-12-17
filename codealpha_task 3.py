import pygame
import random
import time
import os

# Verify the contents of the directory
image_dir = r"C:\Users\admin\OneDrive\Desktop\python game"
print("Files in directory:", os.listdir(image_dir))

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CARD_SIZE = (100, 150)
CARD_MARGIN = 10
BACKGROUND_COLOR = (50, 50, 50)
FPS = 30
HIGH_SCORE_FILE = os.path.join(image_dir, "high_score.txt")

# Define levels
levels = {
    'easy': {'grid_size': (2, 2), 'time_limit': 2 * 60, 'num_pairs': 2},   # 2 pairs of cards (4 cards total)
    'medium': {'grid_size': (4, 3), 'time_limit': 4 * 60, 'num_pairs': 6}, # 6 pairs of cards (12 cards total)
    'hard': {'grid_size': (4, 4), 'time_limit': 5 * 60, 'num_pairs': 8}    # 8 pairs of cards (16 cards total)
}

# Function to get the high score from the file
def get_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, 'r') as file:
            return int(file.read().strip())
    return 0

# Function to save the high score to the file
def save_high_score(score):
    with open(HIGH_SCORE_FILE, 'w') as file:
        file.write(str(score))

# Load sounds
def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

# Function to load images
def load_images(num_pairs):
    card_images = []
    for i in range(1, num_pairs + 1):
        image_path = os.path.join(image_dir, f"card_{i}.jpg.jpg")
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, CARD_SIZE)  # Scale the image to fit the card size
        card_images.append(image)
        card_images.append(image)  # Create a pair of each image
    random.shuffle(card_images)
    return card_images

# Function to create card positions
def create_card_positions(grid_size):
    cols, rows = grid_size
    x_margin = (SCREEN_WIDTH - (cols * (CARD_SIZE[0] + CARD_MARGIN)) + CARD_MARGIN) // 2
    y_margin = (SCREEN_HEIGHT - (rows * (CARD_SIZE[1] + CARD_MARGIN)) + CARD_MARGIN) // 2
    positions = [(x_margin + col * (CARD_SIZE[0] + CARD_MARGIN), 
                  y_margin + row * (CARD_SIZE[1] + CARD_MARGIN)) 
                 for row in range(rows) for col in range(cols)]
    return positions

# Function to display the level selection menu
def select_level():
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Ensure screen is defined here
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.Font(None, 74)
    easy_text = font.render("Easy", True, (255, 255, 255))
    medium_text = font.render("Medium", True, (255, 255, 255))
    hard_text = font.render("Hard", True, (255, 255, 255))

    screen.blit(easy_text, (SCREEN_WIDTH // 2 - easy_text.get_width() // 2, 150))
    screen.blit(medium_text, (SCREEN_WIDTH // 2 - medium_text.get_width() // 2, 250))
    screen.blit(hard_text, (SCREEN_WIDTH // 2 - hard_text.get_width() // 2, 350))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 150 <= pos[1] <= 150 + easy_text.get_height() and SCREEN_WIDTH // 2 - easy_text.get_width() // 2 <= pos[0] <= SCREEN_WIDTH // 2 + easy_text.get_width() // 2:
                    return 'easy'
                elif 250 <= pos[1] <= 250 + medium_text.get_height() and SCREEN_WIDTH // 2 - medium_text.get_width() // 2 <= pos[0] <= SCREEN_WIDTH // 2 + medium_text.get_width() // 2:
                    return 'medium'
                elif 350 <= pos[1] <= 350 + hard_text.get_height() and SCREEN_WIDTH // 2 - hard_text.get_width() // 2 <= pos[0] <= SCREEN_WIDTH // 2 + hard_text.get_width() // 2:
                    return 'hard'

# Game logic functions
def draw_game(card_images, card_positions, revealed, start_time, game_duration):
    screen.fill(BACKGROUND_COLOR)
    for idx, pos in enumerate(card_positions):
        if revealed[idx]:
            screen.blit(card_images[idx], pos)
        else:
            pygame.draw.rect(screen, (200, 200, 200), (*pos, *CARD_SIZE))

    # Draw timer
    elapsed_time = int(time.time() - start_time)
    remaining_time = game_duration - elapsed_time
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    time_text = font.render(f"Time: {minutes}:{seconds:02}", True, (255, 255, 255))
    screen.blit(time_text, (10, 10))

    pygame.display.flip()

def check_match(card_images, revealed, first_choice, second_choice):
    pygame.time.delay(1000)  # Add a 1 second delay
    if card_images[first_choice] == card_images[second_choice]:
        revealed[first_choice] = True
        revealed[second_choice] = True
        play_sound(os.path.join(image_dir, "match.mp3"))
    else:
        revealed[first_choice] = False
        revealed[second_choice] = False
    return None, None

def check_all_revealed(revealed):
    return all(revealed)

def end_game(start_time, game_duration, high_score):
    elapsed_time = int(time.time() - start_time)
    final_score = max(game_duration - elapsed_time, 0)
    if final_score > high_score:
        high_score = final_score
        save_high_score(high_score)
    play_sound(os.path.join(image_dir, "game_over.mp3"))

    # Display scores on the screen
    screen.fill(BACKGROUND_COLOR)
    score_text = font.render(f"Game Over! Your score: {final_score}", True, (255, 255, 255))
    high_score_text = font.render(f"High score: {high_score}", True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    # Delay to display the score before quitting
    pygame.time.delay(5000)

# Main game function
def main():
    global screen, font
    # Initialize the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 36)
    
    # Level selection
    level = select_level()
    config = levels[level]
    card_images = load_images(config['num_pairs'])
    card_positions = create_card_positions(config['grid_size'])
    game_duration = config['time_limit']
    revealed = [False] * len(card_images)
    first_choice = None
    second_choice = None
    start_time = time.time()
    high_score = get_high_score()

    # Main game loop
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                play_sound(os.path.join(image_dir, "click.mp3"))
                for idx, card_pos in enumerate(card_positions):
                    if (card_pos[0] < pos[0] < card_pos[0] + CARD_SIZE[0] and
                            card_pos[1] < pos[1] < card_pos[1] + CARD_SIZE[1]):
                        if not revealed[idx]:
                            if first_choice is None:
                                first_choice = idx
                                revealed[first_choice] = True
                            elif second_choice is None:
                                second_choice = idx
                                revealed[second_choice] = True
                                first_choice, second_choice = check_match(card_images, revealed, first_choice, second_choice)

        draw_game(card_images, card_positions, revealed, start_time, game_duration)
        clock.tick(FPS)

        if check_all_revealed(revealed) or time.time() - start_time >= game_duration:
            end_game(start_time, game_duration, high_score)
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()