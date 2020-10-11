import numpy as np 
import pygame 
bg_filepath = "rocket_sprite/background.png"

bg = pygame.image.load(bg_filepath)
bg_width = bg.get_width() 
bg_height = bg.get_height() 

pygame.init() 

class Rocket: 
    def __init__(self, filepath_rocket): 
        self.x = 250 - 25 
        self.y0 = 600 #To begin with 
        self.y = self.y0
        self.im_rocket = [pygame.image.load(name) for name in filepath_rocket]

        self.width = self.im_rocket[0].get_width() 
        self.height = self.im_rocket[0].get_height() 

    def move(self, keys): #Need only for testing
        if keys[pygame.K_UP] and self.y > 0: 
            self.y -= 5
        if keys[pygame.K_DOWN] and self.y + self.height < bg_height: 
            self.y += 5
        
    def draw(self, win): 
        ch = np.random.randint(1, 3)
        win.blit(self.im_rocket[ch], (self.x, self.y, self.width, self.height))

fpath_rockets = ["rocket_sprite/rocket_base.png", "rocket_sprite/rocket_1.png", "rocket_sprite/rocket_2.png"]
R1 = Rocket(fpath_rockets)

win = pygame.display.set_mode((bg_width, bg_height)) #Width and hight of window
pygame.display.set_caption("Rocket Game") #Name of window 

#Main loop:
run = True 
while run: 
    pygame.time.delay(20) #100 ms

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: #If exit button is pressed, do this statement
            run = False 

    keys = pygame.key.get_pressed() 
    win.blit(bg, (0,0))
    R1.move(keys) 
    R1.draw(win) 
    
    pygame.display.update()