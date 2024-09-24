import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

BLOCK_NUMBER = 10
# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the font
font = pygame.font.Font(None, 36)

# Set up the game variables
numbers = list(range(1, BLOCK_NUMBER + 1))  # Numbers 1 to 10
random.shuffle(numbers)
hidden = False
selected = []
won = False
current_number = 2  # Track the current number to click
game_over = False
start_time = time.time()
stop_time = None

# Create a grid to store the positions of the numbers
grid = []
spacing = 10  # Define spacing around each block
number_positions = {}  # Dictionary to store number positions

while len(grid) < BLOCK_NUMBER:  # Create 10 blocks
    x = random.randint(0 + spacing, WIDTH - 90 - spacing)  # Random x position with spacing
    y = random.randint(0 + spacing, HEIGHT - 90 - spacing)  # Random y position with spacing
    new_position = (x, y)
    # Check for overlap with spacing
    if all(not (abs(new_position[0] - pos[0]) < 90 + spacing and abs(new_position[1] - pos[1]) < 90 + spacing) for pos in grid):
        grid.append(new_position)

# Populate the dictionary with positions and corresponding numbers
for i in range(len(grid)):
    number_positions[grid[i]] = numbers[i]

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not hidden:
            # Check if the first number is clicked
            pos = pygame.mouse.get_pos()
            for position in grid:
                rect = pygame.Rect(position[0], position[1], 90, 90)
                if rect.collidepoint(pos):
                    number = number_positions[position]
                    if number == 1:
                        hidden = True  # Hide numbers after clicking the first one
                        grid.remove(position)
                        number_positions.pop(position)
                    else:
                        hidden = False
        elif event.type == pygame.MOUSEBUTTONDOWN and hidden:
            pos = pygame.mouse.get_pos()
            for position in grid:
                
                rect = pygame.Rect(position[0], position[1], 90, 90)
                if rect.collidepoint(pos):
                    number = number_positions[position]
                    if number == current_number:
                        selected.append(number)
                        grid.remove(position)
                        number_positions.pop(position)
                        current_number += 1
                        if current_number > len(numbers):  # Check if game is won
                            won = True  # User has clicked all numbers in order
                            game_over = True
                            stop_time = time.time()
                    else:
                        game_over = True
        elif event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                # Restart the game
                hidden = False
                selected = []
                won = False
                current_number = 2
                game_over = False
                numbers = list(range(1, BLOCK_NUMBER + 1))  # Numbers 1 to 10
                start_time = time.time()
                stop_time = None
                random.shuffle(numbers)
                grid = []
                while len(grid) < BLOCK_NUMBER:  # Create 10 blocks
                    x = random.randint(0 + spacing, WIDTH - 90 - spacing)  # Random x position with spacing
                    y = random.randint(0 + spacing, HEIGHT - 90 - spacing)  # Random y position with spacing
                    new_position = (x, y)
                    # Check for overlap with spacing
                    if all(not (abs(new_position[0] - pos[0]) < 90 + spacing and abs(new_position[1] - pos[1]) < 90 + spacing) for pos in grid):
                        grid.append(new_position)
                number_positions = {}  # Dictionary to store number positions
                for i in range(len(grid)):
                    number_positions[grid[i]] = numbers[i]
            elif event.key == pygame.K_q:
                # Quit the game
                running = False

    # Draw everything
    screen.fill(BLACK)  # Change background to black
    if not game_over:
        for position in grid:
            if not hidden:  # Only draw text if not hidden
                rect = pygame.Rect(position[0], position[1], 90, 90)  # Draw white block background
                pygame.draw.rect(screen, WHITE, rect, 0)  # Draw the block background
                text = font.render(str(number_positions[position]), True, BLACK)  # Change text color to BLACK
                text_rect = text.get_rect(center=(position[0] + 45, position[1] + 45))
                screen.blit(text, text_rect)  # Draw the number on top of the block
            else:
                rect = pygame.Rect(position[0], position[1], 90, 90)
                pygame.draw.rect(screen, WHITE, rect, 0)  # Change covered blocks to white
        if won:
            text = font.render("You Won!", True, GREEN)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
        else:
            text = font.render(f'{(time.time() - start_time):.1f} seconds', True, WHITE)
            text_rect = text.get_rect(top=10, left=10)
            screen.blit(text, text_rect)
    else:
        if won:
            text = font.render(f'You Won! Total duration: {(stop_time - start_time):.1f} seconds', True, GREEN)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
            screen.blit(text, text_rect)
        else:
            text = font.render("Game Over", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
            screen.blit(text, text_rect)
            
            text = font.render("Press 'R' to restart or 'Q' to quit", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
        text = font.render("Press 'R' to restart or 'Q' to quit", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()