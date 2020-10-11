import pygame 
import numpy as np

pygame.init() #Always need to do this. 

win_height = 500 
win_width = 300
win = pygame.display.set_mode((win_width, win_height)) #Width and hight of window

pygame.display.set_caption("First Game") #Name of window 

width = 50
height = 115 
x = 50 
y = win_height - height-10 


left = False
right = False 
walk_count = 0

file_names_walk = ["rocket_sprite/rocket_1.png", "rocket_sprite/rocket_2.png"]
file_name_standstill = "rocket_sprite/rocket_base.png"
walkRight = [pygame.image.load(name) for name in file_names_walk]
walkLeft = [pygame.image.load(name) for name in file_names_walk]
char = pygame.image.load(file_name_standstill)

isJump = False
jumpCount = 10
v = 5 

def redrawGameWindow(): 
    global walk_count
    #win.blit(background_image, (0,0)) to draw background. 
    win.fill((0,0,0))#Fill the window before drawing a new rectangle. 
    #               window,    RGB,     pos       shape
    #pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    if walk or isJump:
        im_count = np.random.randint(0, 2)
        win.blit(walkRight[im_count], (x,y, width, height))
    else: 
        win.blit(char, (x,y, width, height))
    pygame.display.update()

#Main loop:
run = True 
while run: 
    pygame.time.delay(20) #100 ms

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: #If exit button is pressed, do this statement
            run = False 

    keys = pygame.key.get_pressed() 

    walk = False
    if keys[pygame.K_LEFT] and x > 0: 
        x -= v
        walk = True
    if keys[pygame.K_RIGHT] and x + width < win_width: 
        x += v
        walk = True
    if not isJump:
        if keys[pygame.K_SPACE]: 
                isJump = True     
        
    else: 
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= jumpCount**2 * 0.5 *neg
            jumpCount -= 1
        else: 
            isJump = False
            jumpCount = 10
    redrawGameWindow()

pygame.quit() 
