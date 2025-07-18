import pygame
import sys

# --- Initialization ---
pygame.init()

# Constants
WIDTH, HEIGHT = 1920, 1000
FPS = 60
BG_COLOR = (30, 30, 30)

# Create the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sneak Cheat")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# --- Game Loop ---
running = True
while running:
    clock.tick(FPS)  # Limit frame rate

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        

    # --- Game Logic ---
    # Update your game state here
    

    # --- Drawing ---
    screen.fill(BG_COLOR)

    # Draw your game elements here

    pygame.display.flip()  # Update the screen

# --- Clean Up ---
pygame.quit()
sys.exit()
