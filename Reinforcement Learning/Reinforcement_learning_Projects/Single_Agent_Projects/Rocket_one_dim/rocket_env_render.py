import numpy as np 
import pygame 

class Render_Rocket: 
    def __init__(self, h_bot, h_top): 
        bg_filepath = "Reinforcement_learning_Projects/Single_Agent_Projects/Rocket_one_dim/rocket_sprite/background.png"
        r0_sprite = "Reinforcement_learning_Projects/Single_Agent_Projects/Rocket_one_dim/rocket_sprite/rocket_base_v2.png"
        r1_sprite = "Reinforcement_learning_Projects/Single_Agent_Projects/Rocket_one_dim/rocket_sprite/rocket_1_v2.png"
        r2_sprite = "Reinforcement_learning_Projects/Single_Agent_Projects/Rocket_one_dim/rocket_sprite/rocket_2_v2.png"

        self.bg = pygame.image.load(bg_filepath)
        self.bg_width = self.bg.get_width() 
        self.bg_height = self.bg.get_height() 

        self.x = 250 - 25 
        self.y0 = 600 #To begin with 
        self.y = self.y0
        self.im_rocket = [r0_sprite, r1_sprite, r2_sprite]
        self.im_rocket = [pygame.image.load(name) for name in self.im_rocket]

        self.width = self.bg_width
        self.height = self.bg_height 
        self.find_height = lambda h: self.height - self.im_rocket[0].get_height() - int((h-h_bot)/h_top*(self.height-self.im_rocket[0].get_height()))

    def move(self, win, x, y, action): #Need only for testing
        self.y = y 
        self.draw(win, action)
        
    def draw(self, win, action): 
        if action == 0: 
            ch = 0 
        else: 
            ch = np.random.randint(1, 3)
        win.blit(self.bg, (0,0))
        win.blit(self.im_rocket[ch], (self.x, self.y, self.width, self.height))
        pygame.draw.line(win, (0,0,0), (220, self.find_height(self.target)), (260, self.find_height(self.target)), 2)
        pygame.display.update()

    def render_env(self, heights, actions, target): 
        self.target = target
        pygame.init() 
        win = pygame.display.set_mode((self.bg_width, self.bg_height)) #Width and hight of window
        pygame.display.set_caption("Rocket Game") #Name of window 

        self.move(win, 225, self.find_height(heights[0]), actions[0])
        done = False
        for height, action in zip(heights[1:], actions[1:]):
            pygame.time.delay(10) #10 ms
            self.move(win, 225, self.find_height(height), action)
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: #If exit button is pressed, do this statement
                    done = True 
            if done: 
                break

        pygame.quit()

    