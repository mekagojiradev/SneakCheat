import pygame
import sys
import random

# --- Initialization ---
pygame.init()

# Constants
WIDTH, HEIGHT = 1920, 1000
FPS = 60
BG_COLOR = (30, 30, 30)

# Variables
safeTime = 0
teacherTime = 0
safeTimeMin = 1 * FPS
safeTimeMax = 8 * FPS
teacherTimeMin = 2 * FPS
teacherTimeMax = 10 * FPS
score = 0
running = True
isTeacherLooking = False
isCheating = False
mainMenu = False
playingGame = True
gameOver = False
font = pygame.font.SysFont(None, 36)

# Functions
def setSafeTime():
    global safeTime
    safeTime = random.randint(safeTimeMin,safeTimeMax)

def setTeacherTime():
    global teacherTime 
    teacherTime = random.randint(teacherTimeMin, teacherTimeMax)

def startGame():
    mainMenu = False
    playingGame = True
    setSafeTime()

def drawTeacher():
    if isTeacherLooking:
        pygame.draw.rect(screen, (255,0,0), (WIDTH/2,HEIGHT/2,50,50))
    elif not isTeacherLooking:
        if safeTime > (FPS / 2):
            pygame.draw.rect(screen, (0,255,0), (WIDTH/2,HEIGHT/2,50,50))
        else:
            pygame.draw.rect(screen, (255,255,0), (WIDTH/2,HEIGHT/2,50,50))

def drawGameOver():
    text_surface = font.render('Game Over!', True, (255, 0, 0))
    screen.blit(text_surface, (WIDTH/2, HEIGHT/2))

def drawScore():
    text_surface = font.render('Score: '+ str(score), True, (255, 255, 255))
    screen.blit(text_surface, (WIDTH/2, 200))

# Create the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sneak Cheat")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# --- Game Loop ---
while running:
    clock.tick(FPS)  # Limit frame rate

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if playingGame and pygame.mouse.get_pressed(3)[0] == True:
        isCheating = True
        score += 1
    else:
        isCheating = False    

    # --- Game Logic ---
    # Update your game state here
    
    if isCheating and isTeacherLooking:
        gameOver = True
        playingGame = False


    if playingGame and not isTeacherLooking:
        if safeTime <= 0:
           isTeacherLooking = True
           setTeacherTime()
        else: 
            safeTime -= 1
    elif playingGame and isTeacherLooking:
        if teacherTime <= 0:
            isTeacherLooking = False
            setSafeTime()
        else:
            teacherTime -= 1

    # --- Drawing ---
    screen.fill(BG_COLOR)
    # Draw your game elements here
    if playingGame:
        drawTeacher()
        drawScore()
    elif gameOver:
        drawGameOver()
        drawScore()

    pygame.display.flip()  # Update the screen

# --- Clean Up ---
pygame.quit()
sys.exit()
