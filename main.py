import pygame
import sys
import random
import sound
import button
from player import Player

# --- Initialization ---
pygame.init()

# Constants
WIDTH, HEIGHT = 1920, 1000
FPS = 60
BG_COLOR = (30, 30, 30)
SHOP_MARGIN_RIGHT = 340
SHOP_X = 260
SHOP_WIDTH = WIDTH - SHOP_X - SHOP_MARGIN_RIGHT

# Variables
safeTime = 0
teacherTime = 0
safeTimeMin = 1 * FPS
safeTimeMax = 8 * FPS
teacherTimeMin = 2 * FPS
teacherTimeMax = 10 * FPS
score = 0
scoreMultiplier = 1
money = 0
testTimeForMoney = 15 * FPS
timesAllowanceApplied = 0
running = True
isTeacherLooking = False
isCheating = False
mainMenu = True
playingGame = False
gameOver = False
inShop = False
justEnteredShop = False


# Fonts
font = pygame.font.SysFont("Courier New", 25)
small_font = pygame.font.SysFont("Courier New", 18)
sleeping_font = pygame.font.SysFont(None, 35)

background_occupied = []
background_colors = []
warningTime = 0
showWarning = False
teacherBlinking = False
blinkMultiplier = 1
blinkCounter = 0
hatBought = False
pencilBought = False
testBought = False
glassesBought = False
mixer = sound.Mixer()
YELL_VOLUME = 0.3
DIR = 'assets/buttons/'
leaderBoard = [Player('Satan', 9999), 
                    Player('Rihanna',4880), 
                    Player('Dunkey', 3500),
                    Player('Carrot Top', 1450),
                    Player('Shania Twain', 500)]
shopPrices = [('Last Years Tests', '$13'),
              ('Faster Writing Pencil', '$16'),
              ('Academic Integrity Hat', '$7'),
              ('Shady Glasses', '$4')]

wasClicking = False
musicNotStarted = True

# Shirt colors used for background students
shirt_colors = [
    (120, 120, 120),  # gray
    (100, 50, 50),    # faded red
    (70, 90, 90),     # dusty teal
    (80, 80, 110),    # muted blue
    (110, 85, 40),    # tan/brown
]

# Create the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sneak Cheat")

# Create Buttons
start_img = pygame.image.load(f'{DIR}start_button.jpeg').convert_alpha()
start_img_alt = pygame.image.load(f'{DIR}start_button_white.jpeg').convert_alpha()

menu_btn_img_blk = pygame.image.load(f'{DIR}main_menu_blk.jpeg').convert_alpha() 
menu_btn_img_alt = pygame.image.load(f'{DIR}main_menu_w.jpeg').convert_alpha() 

try_again_img_blk = pygame.image.load(f'{DIR}try_again_blk.jpeg').convert_alpha()
try_again_img_alt = pygame.image.load(f'{DIR}try_again_w.jpeg').convert_alpha()

quit_img_blk = pygame.image.load(f'{DIR}quit_b.jpeg').convert_alpha()
quit_img_alt = pygame.image.load(f'{DIR}quit_w.jpeg').convert_alpha()

#Shop
shop_img_w = pygame.image.load(f'{DIR}shop_w.jpeg').convert_alpha() 
shop_img_r = pygame.image.load(f'{DIR}shop_r.jpeg').convert_alpha() 
exit_img_w = pygame.image.load(f'{DIR}exit_w.jpeg').convert_alpha() 
exit_img_r = pygame.image.load(f'{DIR}exit_r.jpeg').convert_alpha() 
pencil_img = pygame.image.load(f'{DIR}pencil.png').convert_alpha() 
tests_img = pygame.image.load(f'{DIR}tests.png').convert_alpha() 
glasses_img = pygame.image.load(f'{DIR}glasses.png').convert_alpha() 
ai_img = pygame.image.load(f'{DIR}ai.png').convert_alpha() 
shop_bg = pygame.image.load(f"{DIR}shop_back.png").convert()

shop_bg = pygame.transform.scale(shop_bg,screen.get_size())
# ALTS
pencil_img_out = pygame.image.load(f'{DIR}pencil_out.png').convert_alpha() 
tests_img_out = pygame.image.load(f'{DIR}tests_out.png').convert_alpha() 
glasses_img_out = pygame.image.load(f'{DIR}glasses_out.png').convert_alpha() 
ai_img_out = pygame.image.load(f'{DIR}ai_out.png').convert_alpha() 
pencil = button.Button(screen, pencil_img, x=WIDTH//3-150,y=(2/3)*HEIGHT , scale=1, image_alt=pencil_img)  
tests = button.Button(screen, tests_img, x=WIDTH//2-450,y=(2/5)*HEIGHT , scale=1.3, image_alt=tests_img)  
glasses = button.Button(screen, glasses_img, x=WIDTH//2,y=(2/5)*HEIGHT , scale=1.5, image_alt=glasses_img)  
ai_hat = button.Button(screen, ai_img, x=WIDTH//2,y=(2/3)*HEIGHT , scale=1.5, image_alt=ai_img)  

shopButton = button.Button(screen, shop_img_w, x=WIDTH//4,y=(2/3)*HEIGHT + 250, scale=0.3, image_alt=shop_img_r)  
exitButton = button.Button(screen, exit_img_w, x=WIDTH//2,y=(2/3)*HEIGHT + 250, scale=0.3, image_alt=exit_img_r)  

startButton = button.Button(screen, start_img, x=WIDTH//2,y=(2/3)*HEIGHT, scale=0.3, image_alt=start_img_alt)
quitButton = button.Button(screen, quit_img_blk, x=WIDTH//2,y=(2/3)*HEIGHT + 100, scale=0.4, image_alt=quit_img_alt) 

menuButton = button.Button(screen, menu_btn_img_blk, x=WIDTH//2 - 200,y=(2/3)*HEIGHT, scale=0.3, image_alt=menu_btn_img_alt) 
tryAgainButton = button.Button(screen, try_again_img_blk, x=WIDTH//2 + 200,y=(2/3)*HEIGHT, scale=0.3, image_alt=try_again_img_alt) 



# Clock for controlling frame rate
clock = pygame.time.Clock()

# Generate background desk data once at startup
background_occupied = [random.random() < 0.5 for _ in range(6)]
background_colors = [random.choice(shirt_colors) for _ in range(6)]

def setSafeTime():
    global safeTime, warningTime, showWarning, teacherBlinking
    safeTime = random.randint(safeTimeMin, safeTimeMax)
    warningTime = int(safeTime * 0.2)
    showWarning = False
    teacherBlinking = False

def setTeacherTime():
    global teacherTime 
    teacherTime = random.randint(teacherTimeMin, teacherTimeMax)

def startGame():

    global mainMenu, playingGame, score, money, timesAllowanceApplied, gameOver, isTeacherLooking
    #Also restetting item stuff
    global blinkMultiplier, scoreMultiplier, teacherTimeMin, teacherTimeMax, testTimeForMoney, hatBought, testBought, pencilBought, glassesBought

    mainMenu = False
    playingGame = True
    gameOver = False
    score = 0
    money = 50
    timesAllowanceApplied = 0
    blinkMultiplier = 1
    scoreMultiplier = 1
    teacherTimeMin = 2 * FPS
    teacherTimeMax = 10 * FPS
    testTimeForMoney = 15 * FPS
    hatBought, testBought, pencilBought, glassesBought = False, False, False, False

    isTeacherLooking = False
    
    setSafeTime()
    mixer.ring_bell(volume=.1)
    mixer.set_music(isPlaying=True)

def resumeGame():
    global mainMenu, playingGame, score, money, timesAllowanceApplied, gameOver, isTeacherLooking


    mainMenu = False
    playingGame = True
    gameOver = False
    # isTeacherLooking = False
    
    setSafeTime()
    mixer.set_music(isPlaying=True)
       
def startMenu():
    global mainMenu, playingGame, score, gameOver, isTeacherLooking
    mainMenu = True
    playingGame = False
    gameOver = False
    isTeacherLooking = False
    score = 0
    setSafeTime()
    mixer.set_music(start=True)
    

    
def setShop() -> None:
    global playingGame, inShop, justEnteredShop
    inShop = True
    playingGame = False
    mixer.set_music(isShop=True)
    # setSafeTime()
    
    
   
# Will Use Pygbag to check cache for previous data   
def setLeaderBoard():
    global leaderBoard 
    leaderBoard = [Player('Satan', 9999), 
                    Player('Rihanna',4880), 
                    Player('Dunkey', 3500),
                    Player('Carrot Top', 1450),
                    Player('Shania Twain', 500)]

def drawShop():
    global inShop, pencil, glasses, ai_hat, tests, exitButton
  
    shopButton.draw(hide=True)
    shop_overlay = pygame.Surface((SHOP_WIDTH, HEIGHT - 400))
    shop_overlay.fill((90, 60, 20))
    screen.blit(shop_overlay, (SHOP_X, 200))
    # Foreground layer
    shop_overlay = pygame.Surface((SHOP_WIDTH, HEIGHT - 420))
    shop_overlay.fill((15, 80, 25))

    
   
   
    # afford messafe
    not_afford = font.render("Can't Afford!", True, (255, 255, 255))
    not_afford_rect = not_afford.get_rect(center=(885 + 75, 500))  # center of the 150x65 box
    nice = font.render("       Nice!        ", True, (255, 255, 255))
    nice_rect = nice.get_rect(center=(885 + 75, 500))
    
  
    
    screen.blit(shop_overlay, (SHOP_X, 210))


    if pencil.draw():
    
        if buyPencil():    
            pencil = button.Button(screen, pencil_img_out, x=WIDTH//3-150,y=(2/3)*HEIGHT , scale=1, image_alt=pencil_img_out) 
            screen.blit(nice, nice_rect) 
            mixer.cha_ching(volume=.5)
        else:
            # print cant afford
            # pencil = button.Button(screen, pencil_img_out, x=WIDTH//3-300,y=(2/3)*HEIGHT , scale=2, image_alt=pencil_img_out)  
            screen.blit(not_afford, not_afford_rect) if not pencilBought else None

    if glasses.draw():
        
        if buyGlasses():
            screen.blit(nice, nice_rect) 
            glasses = button.Button(screen, glasses_img_out, x=WIDTH//2+100,y=(2/5)*HEIGHT , scale=1.5, image_alt=glasses_img_out)
            mixer.cha_ching(volume=.5)
        else:
            # cant afford
            # glasses = button.Button(screen, glasses_img_out, x=WIDTH//2+300,y=(1/4)*HEIGHT , scale=2, image_alt=glasses_img_out)
            screen.blit(not_afford, not_afford_rect) if not glassesBought else None
            
            
    if ai_hat.draw():
        
        if buyHat():
            screen.blit(nice, nice_rect) 
            ai_hat = button.Button(screen, ai_img_out, x=WIDTH//2+100,y=(2/3)*HEIGHT , scale=1.5, image_alt=ai_img_out)
            mixer.cha_ching(volume=.5)
        else:
            # can't afford
            # ai_hat = button.Button(screen, ai_img_out, x=WIDTH//2+300,y=(2/3)*HEIGHT , scale=2, image_alt=ai_img_out)
            screen.blit(not_afford, not_afford_rect) if not hatBought else None
            
            
    if tests.draw():
       
        if buyTest():
            screen.blit(nice, nice_rect) 
            tests = button.Button(screen, tests_img_out, x=WIDTH//2-480,y=(2/5)*HEIGHT - 15 , scale=1.3, image_alt=tests_img_out)  
            mixer.cha_ching(volume=.5)
            
        else:
            # can't afford
            # tests = button.Button(screen, tests_img_out, x=WIDTH//2-450,y=(1/4)*HEIGHT , scale=2, image_alt=tests_img_out)  
            screen.blit(not_afford, not_afford_rect) if not testBought else None
            
      
    price_font = pygame.font.SysFont("Courier New", 26)
    price_color = (255, 255, 255)  # Yellowish for visibility

    price_start_x = SHOP_X + SHOP_WIDTH - 250  # Push prices toward right side
    price_start_y = 240  # Start near top of chalkboard
    line_spacing = 60  # Space between each line

    for i, (item, price) in enumerate(shopPrices):
        item_surface = price_font.render(f"{item}", True, (255, 255, 255))
        price_surface = price_font.render(f"{price}", True, price_color)

        screen.blit(item_surface, (price_start_x - 170, price_start_y + i * line_spacing))
        screen.blit(price_surface, (price_start_x + 200, price_start_y + i * line_spacing))  # push $ amount further right

    if exitButton.draw():
        inShop = False
        resumeGame()
    

def buyHat():
    global money, teacherTimeMin, teacherTimeMax, hatBought
    if money >= 7 and not hatBought:
        money -= 7
        teacherTimeMin = 1 * FPS
        teacherTimeMax = 7 * FPS
        hatBought = True

def buyTest():
    global money, scoreMultiplier, testBought
    if money >= 13 and not testBought:
        money -= 13
        scoreMultiplier *= 2
        testBought = True

def buyPencil():
    global money, testTimeForMoney, pencilBought
    if money >= 16 and not pencilBought:
        money -= 16
        testTimeForMoney = 10 * FPS
        pencilBought = True

def buyGlasses():
    global money, blinkMultiplier, glassesBought
    if money >= 4 and not glassesBought:
        money -=4
        blinkMultiplier = 2
        glassesBought = True

def drawTeacher():
    teacher_x = WIDTH // 2 - 30
    floor_y = int(HEIGHT * 0.65)
    teacher_y = floor_y - 140

    body_color = (255, 0, 0) if isTeacherLooking else (0, 128, 0)

    pygame.draw.rect(screen, (255, 224, 189), (teacher_x + 10, teacher_y, 40, 40))
    pygame.draw.rect(screen, body_color, (teacher_x, teacher_y + 40, 60, 60))
    pygame.draw.rect(screen, (0, 0, 0), (teacher_x, teacher_y + 100, 20, 40))
    pygame.draw.rect(screen, (0, 0, 0), (teacher_x + 40, teacher_y + 100, 20, 40))

    desk_x = WIDTH // 2 - 80
    desk_y = floor_y - 60
    pygame.draw.rect(screen, (139, 69, 19), (desk_x, desk_y, 160, 20))
    pygame.draw.rect(screen, (139, 69, 19), (desk_x, desk_y + 20, 10, 60))
    pygame.draw.rect(screen, (139, 69, 19), (desk_x + 150, desk_y + 20, 10, 60))

    if isTeacherLooking:
        pygame.draw.circle(screen, (0, 0, 0), (teacher_x + 20, teacher_y + 15), 4)
        pygame.draw.circle(screen, (0, 0, 0), (teacher_x + 40, teacher_y + 15), 4)
    elif teacherBlinking and blinkCounter % 30 < 15:
        pygame.draw.circle(screen, (0, 0, 0), (teacher_x + 20, teacher_y + 15), 4)
        pygame.draw.circle(screen, (0, 0, 0), (teacher_x + 40, teacher_y + 15), 4)
    

    if showWarning and blinkCounter % 30 < 15:
        warning_font = pygame.font.SysFont(None, 50)
        warning_surface = warning_font.render('!', True, (255, 0, 0))
        
        screen.blit(warning_surface, (teacher_x - 5, teacher_y - 30))
    elif not isTeacherLooking:
        sleeping_surface = sleeping_font.render('zZz', True, (0, 0, 255))
        screen.blit(sleeping_surface, (teacher_x-5, teacher_y - 25))


def drawStudent():
    student_x = WIDTH // 2 - 300
    student_y = int(HEIGHT * 0.65) + 80

    pygame.draw.rect(screen, (139, 69, 19), (student_x, student_y + 50, 120, 20))
    pygame.draw.rect(screen, (139, 69, 19), (student_x, student_y + 70, 10, 40))
    pygame.draw.rect(screen, (139, 69, 19), (student_x + 110, student_y + 70, 10, 40))

    pygame.draw.rect(screen, (0, 0, 255), (student_x + 40, student_y, 40, 50))
    pygame.draw.rect(screen, (255, 224, 189), (student_x + 45, student_y - 30, 30, 30))
    
    # Highlights the desk when cheating
    if isCheating:
        pygame.draw.rect(screen, (255, 255, 100), (student_x, student_y + 50, (score % testTimeForMoney)//(testTimeForMoney/120), 20), 5)

def drawEmptyDesks():
    desk_width = 120
    desk_height = 20
    leg_height = 40
    leg_width = 10

    base_y = int(HEIGHT * 0.65) + 80 + 50
    center_x = WIDTH // 2 - 300
    offsets = [-400, -200, 200, 400, 600, 800]

    for i, offset in enumerate(offsets):
        x = center_x + offset
        y = base_y

        pygame.draw.rect(screen, (139, 69, 19), (x, y, desk_width, desk_height))
        pygame.draw.rect(screen, (139, 69, 19), (x, y + desk_height, leg_width, leg_height))
        pygame.draw.rect(screen, (139, 69, 19), (x + desk_width - leg_width, y + desk_height, leg_width, leg_height))
        # Randomly places the background students
        if background_occupied[i]:
            drawBackgroundStudent(x, y, background_colors[i])

def drawBackgroundStudent(x, y, color):
    pygame.draw.rect(screen, color, (x + 40, y - 50, 40, 50))
    pygame.draw.rect(screen, (255, 224, 189), (x + 45, y - 80, 30, 30))

def drawClassroom():
    wall_height = int(HEIGHT * 0.65)
    floor_y = wall_height
    floor_height = HEIGHT - wall_height

    pygame.draw.rect(screen, (205, 200, 190), (0, 0, WIDTH, wall_height))
    pygame.draw.rect(screen, (160, 140, 120), (0, wall_height, WIDTH, floor_height))

    chalkboard_width = 500
    chalkboard_height = 200
    chalkboard_x = WIDTH // 2 - chalkboard_width // 2
    chalkboard_y = floor_y - chalkboard_height - 100

    pygame.draw.rect(screen, (15, 80, 25), (chalkboard_x, chalkboard_y, chalkboard_width, chalkboard_height))
    pygame.draw.rect(screen, (90, 60, 20), (chalkboard_x, chalkboard_y, chalkboard_width, 8))
    pygame.draw.rect(screen, (90, 60, 20), (chalkboard_x, chalkboard_y + chalkboard_height - 8, chalkboard_width, 8))

    window_width = 80
    window_height = 180
    window_y = chalkboard_y + 10
    spacing_from_board = 100

    left_start = chalkboard_x - window_width - spacing_from_board
    right_start = chalkboard_x + chalkboard_width + spacing_from_board

    # Draw the windows to the left and right of the chalkboard
    for i in range(3):
        x_left = left_start - i * (window_width + 20)
        x_right = right_start + i * (window_width + 20)
        for x in [x_left, x_right]:
            pygame.draw.rect(screen, (180, 220, 255), (x, window_y, window_width, window_height))
            pygame.draw.rect(screen, (100, 100, 100), (x, window_y, window_width, window_height), 3)
            pygame.draw.line(screen, (220, 240, 255), (x + window_width // 2, window_y), (x + window_width // 2, window_y + window_height), 2)
            pygame.draw.line(screen, (220, 240, 255), (x, window_y + window_height // 2), (x + window_width, window_y + window_height // 2), 2)

    door_width = 100
    door_height = 220
    door_x = 50
    door_y = floor_y - door_height
    pygame.draw.rect(screen, (120, 90, 40), (door_x, door_y, door_width, door_height))
    pygame.draw.rect(screen, (60, 40, 20), (door_x + 10, door_y + 80, 20, 20))
    
    # practice clicking square :)
    
    pygame.draw.rect(screen, (128, 128, 128), (885, 885, 150, 65))
    text_surface = font.render("Practice:)", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(885 + 75, 885 + 32))  # center of the 150x65 box
    screen.blit(text_surface, text_rect)

    light_color = (255, 255, 210)
    pygame.draw.rect(screen, light_color, (WIDTH // 4 - 80, 20, 160, 15))
    pygame.draw.rect(screen, light_color, (3 * WIDTH // 4 - 80, 20, 160, 15))

    # Clock above the chalkboard
    clock_radius = 30
    clock_x = chalkboard_x + chalkboard_width // 2
    clock_y = chalkboard_y - 60
    pygame.draw.circle(screen, (255, 255, 255), (clock_x, clock_y), clock_radius)
    pygame.draw.circle(screen, (0, 0, 0), (clock_x, clock_y), clock_radius, 2)
    pygame.draw.line(screen, (0, 0, 0), (clock_x, clock_y), (clock_x, clock_y - 15), 2)  # hour hand
    pygame.draw.line(screen, (0, 0, 0), (clock_x, clock_y), (clock_x + 15, clock_y), 2)  # minute hand

def drawGameOver():
    red_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    red_overlay.fill((255, 0, 0, 100))
    screen.blit(red_overlay, (0, 0))

    text_surface = pygame.font.SysFont(None, 100).render('CAUGHT CHEATING!', True, (255, 0, 0))
    screen.blit(text_surface, text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
    menuButton.draw()
    tryAgainButton.draw()
    

def drawScore():
    text_surface = font.render('Score: ' + str(score), True, (255, 255, 255))

    screen.blit(text_surface, ((WIDTH / 2) - 220 , (HEIGHT /2) - 130 ))

def drawMoney():
    global money
    global timesAllowanceApplied
    if score // testTimeForMoney > timesAllowanceApplied:
        timesAllowanceApplied += 1
        money += 5
        mixer.cha_ching(volume=.5)
        # play sound
    text_surface = font.render('Allowance: $' + str(money), True, (255, 255, 255))
    screen.blit(text_surface, ((WIDTH / 2) - 220, (HEIGHT /2) - 80 ))


def drawMainMenu():
    title_font = pygame.font.SysFont("Arial Black", 120)
    title_surface = title_font.render("Sneak Cheat", True, (255, 255, 255))
    screen.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100)))
    
    startButton.draw()
    quitButton.draw()
   
    
    
    

def drawLeaderboard(score: int, board: list = leaderBoard, x: int =(WIDTH / 2)   , y: int = (HEIGHT /2) - 130 , length: int=5) -> None:
    # Draw header
    
    text_surface = small_font.render(f'{"Top Students":<15}{"Scores":<10}', True, (255, 255, 255))
    screen.blit(text_surface, (x,y))
    y+=5
    
    for i in range(length):
        y += 20
        text_surface = small_font.render(f'{board[i]}', True, (255, 255, 255))
        screen.blit(text_surface, (x,y))

def updateLeaderboard(score: int, board: list = leaderBoard):
    
    if score > min(board):
        board[board.index(min(board))] = Player("CHEATER", score)
    board.sort(reverse=True) 
    pass  
   
    
    

# --- Game Loop ---
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (mainMenu and quitButton.draw()):  # Get rid of this conditional and add logic to check if in window
            running = False
            
      
        if musicNotStarted:
            setLeaderBoard()
            mixer.set_music(start=True)
            musicNotStarted = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mainMenu and startButton.draw():
                startGame()  
            elif gameOver:
                if tryAgainButton.draw():
                    startGame() 
                    mixer.yell(stop=True)
                    
                elif menuButton.draw(): 
                    drawMainMenu()
                    mixer.yell(stop=True)
                    startMenu()

        
    shopButtonPressed = shopButton.draw(hide=inShop)
    # starts shop music and open shop menu                
    if playingGame and shopButtonPressed:
        setShop()

    if not shopButtonPressed and playingGame and pygame.mouse.get_pressed()[0] and not(pygame.mouse.get_pos()[0] >= 885 and pygame.mouse.get_pos()[0] <= 1035 and pygame.mouse.get_pos()[1] >= 885 and pygame.mouse.get_pos()[1] <= 950):
        isCheating = True

        score += 1 * scoreMultiplier
       
        if not wasClicking:
            mixer.writing(volume=1.0)
            wasClicking = True
            
    else:
        isCheating = False
        if wasClicking:
            mixer.writing(stop=True)
            wasClicking = False
            
        isCheating = False    

    if isCheating and isTeacherLooking and not shopButtonPressed:
        mixer.writing(stop=True)
        mixer.yell(volume=YELL_VOLUME)
        mixer.set_music(gameOver=True)
        gameOver = True
        playingGame = False

    if playingGame and not isTeacherLooking:
        if safeTime <= 0:

            isTeacherLooking = True
            setTeacherTime()
        else:
            safeTime -= 1
            if safeTime <= warningTime:
                showWarning = True
                teacherBlinking = True
                blinkCounter += 1 * blinkMultiplier

    elif playingGame and isTeacherLooking:
        if teacherTime <= 0:
            isTeacherLooking = False
            
            setSafeTime()
        else:
            teacherTime -= 1
    
     # Logic for shop methods and conditionals    
    if inShop:
        drawShop()

    else:
        screen.fill(BG_COLOR)

        drawClassroom()
        drawEmptyDesks()
        drawTeacher()
        drawStudent()
        
    if mainMenu:
        drawMainMenu()
        # shopButton.draw() # Change this to display shop button at diff time
    elif playingGame:
        drawLeaderboard(score)
        drawScore()
        drawMoney()
        if not inShop:
            shopButton.draw() # Change this to display shop button at diff time
    elif gameOver:
        updateLeaderboard(score)
        drawGameOver()
        drawScore()
        # shopButton.draw() # Change this to display shop button at diff time
    # Display the back buffer
    pygame.display.flip()

# --- Clean Up ---
pygame.quit()
sys.exit()