import pygame
import sys
import random
import sound
import time

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
mixer = sound.Mixer()
wasClicking = False
musicNotStarted = True

# Arguments for the drawing functions - Quick Reference
# pygame.draw.rect(surface, color, rect, width=0, border_radius=0)
# pygame.draw.circle(surface, color, center, radius, width=0)
# pygame.draw.line(surface, color, start_pos, end_pos, width=1)

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

# Arguments for the drawing functions - Quick Reference
# pygame.draw.rect(surface, color, rect, width=0, border_radius=0)
# pygame.draw.circle(surface, color, center, radius, width=0)
# pygame.draw.line(surface, color, start_pos, end_pos, width=1)

def drawTeacher():
    x = WIDTH // 2 - 30
    y = HEIGHT // 2 - 180

    if isTeacherLooking:
        body_color = (255, 0, 0)  # angry red
 
    else:
        body_color = (0, 128, 0)  # calm green
    

    # Head
    pygame.draw.rect(screen, (255, 224, 189), (x + 10, y, 40, 40))  # head

    # Body
    pygame.draw.rect(screen, body_color, (x, y + 40, 60, 60))  # torso

    # Legs
    pygame.draw.rect(screen, (0, 0, 0), (x, y + 100, 20, 40))  # left leg
    pygame.draw.rect(screen, (0, 0, 0), (x + 40, y + 100, 20, 40))  # right leg
  
    # Desk Top
    pygame.draw.rect(screen, (139, 69, 19), (WIDTH//2 - 80, HEIGHT//2 - 80, 160, 20))  # top of desk

    # Desk Legs
    pygame.draw.rect(screen, (139, 69, 19), (WIDTH//2 - 80, HEIGHT//2 - 60, 10, 60))  # left leg
    pygame.draw.rect(screen, (139, 69, 19), (WIDTH//2 + 70, HEIGHT//2 - 60, 10, 60))  # right leg    
            
    # Eyes
    eye_color = (0, 0, 0)
    if isTeacherLooking:
        pygame.draw.circle(screen, eye_color, (x + 20, y + 15), 4)
        pygame.draw.circle(screen, eye_color, (x + 40, y + 15), 4)
    
# Arguments for the drawing functions - Quick Reference
# pygame.draw.rect(surface, color, rect, width=0, border_radius=0)
# pygame.draw.circle(surface, color, center, radius, width=0)
# pygame.draw.line(surface, color, start_pos, end_pos, width=1)

def drawStudent():
    # Desk
    pygame.draw.rect(screen, (139,69,19), (WIDTH//2 - 160, HEIGHT//2 + 130, 120, 20))  # desk top
    pygame.draw.rect(screen, (139,69,19), (WIDTH//2 - 160, HEIGHT//2 + 150, 10, 40))   # desk leg left
    pygame.draw.rect(screen, (139,69,19), (WIDTH//2 - 50, HEIGHT//2 + 150, 10, 40))    # desk leg right

    # Body
    pygame.draw.rect(screen, (0, 0, 255), (WIDTH//2 - 120, HEIGHT//2 + 80, 40, 50))    # student body

    # Head
    pygame.draw.rect(screen, (255, 224, 189), (WIDTH//2 - 115, HEIGHT//2 + 50, 30, 30))  # student head

# Arguments for the drawing functions - Quick Reference
# pygame.draw.rect(surface, color, rect, width=0, border_radius=0)
# pygame.draw.circle(surface, color, center, radius, width=0)
# pygame.draw.line(surface, color, start_pos, end_pos, width=1)

def drawClassroom():
    # Walls
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, WIDTH, HEIGHT * 0.6))  # top wall
    pygame.draw.rect(screen, (180, 180, 180), (0, HEIGHT * 0.6, WIDTH, HEIGHT * 0.4))  # floor

    # Chalkboard
    pygame.draw.rect(screen, (10, 80, 10), (WIDTH//2 - 300, 50, 600, 340))  # chalkboard
    pygame.draw.rect(screen, (60, 40, 0), (WIDTH//2 - 300, 50, 600, 10))    # chalkboard top border

    # Windows
    for i in range(3):
        pygame.draw.rect(screen, (180, 220, 255), (100 + i*200, 100, 80, 80))
        pygame.draw.line(screen, (200, 240, 255), (100 + i*200 + 40, 100), (100 + i*200 + 40, 180), 2)
        pygame.draw.line(screen, (200, 240, 255), (100 + i*200, 140), (180 + i*200, 140), 2)

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
            
    # if gameOver and pygame.mouse.get_pressed(3)[0]: 
    #     startGame()
        
    if musicNotStarted:
        mixer.set_music(isPlaying=True)
        musicNotStarted = False
    
    if playingGame and pygame.mouse.get_pressed(3)[0] == True:
        isCheating = True

        score += 1
       
        if not wasClicking:
            mixer.writing(volume=1.0)
            wasClicking = True
            
    else:
        if wasClicking:
            mixer.writing(stop=True)
            wasClicking = False
            
        isCheating = False    

    # --- Game Logic ---
    # Update your game state here
    
    if isCheating and isTeacherLooking:
        mixer.writing(stop=True)
        mixer.yell()
        mixer.set_music(gameOver=True)
        time.sleep(2)
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
        drawClassroom()
        drawTeacher()
        drawStudent()
        drawScore()
    elif gameOver:
        drawGameOver()
        drawScore()

    pygame.display.flip()  # Update the screen

# --- Clean Up ---
pygame.quit()
sys.exit()
