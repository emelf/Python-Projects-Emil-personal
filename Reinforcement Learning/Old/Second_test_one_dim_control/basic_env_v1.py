# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 10:01:41 2020

@author: Emil Melfald

A 1 dimentional system with constant gravitational force. The agent should choose to either "fire" or "not fire" its engine to get closer to its target. 
"""
import numpy as np 

class one_dim_control(): 
    def __init__(self): 
        self.g = 10 #m/s2 
        self.h_target = 40
        self.h_map = 1000
        self.h_bot = 0
        self.dt = 0.05
        self.h = 0 
        self.v = 0
        self.t_max = 10
        self.eps = 1e-3
        
        self.observation_space = np.array([0,0,0])
        self.action_space = np.arange(0, 20, 1) #Where [no a, small a, some a, large a]
        
    def reset(self): 
        self.done = False
        self.h = 0 
        self.v = 0 
        self.dh = self.h_target - self.h 
        self.t = 0
        return np.array([self.h, self.v, self.dh])
    
    def step(self, action): #Action is boolean values if the veicle is accelerating or not. action = [a, a_not]
        self.v += (self.action_space[action] - self.g)*self.dt
            
        self.h += self.v*self.dt     
        if self.h < self.h_bot-self.eps: 
            self.h = 0 
            self.v = 0
        elif self.h > self.h_map+self.eps: 
            self.h = self.h_map
            self.v = 0
            
        self.dh = self.h_target - self.h 
        self.t += self.dt
        if self.t >= self.t_max: 
            self.done = True
        
        return np.array([self.h, self.v, self.dh]), self.get_reward(), self.done, "Info"
    
    def get_reward(self): 
        """
        if self.dh > 1 or self.dh < -1: 
            return abs(1/self.dh) 
        else: 
            return 1"""
        if self.h <=0 : #Gives extra punishment for 
            return -100*self.dt
        else:
             return -(self.dh**2)/self.h_target**2
        
        

