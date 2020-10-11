# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 10:01:41 2020

@author: Emil Melfald

A 1 dimentional system with constant gravitational force. The agent should choose to either "fire" or "not fire" its engine to get closer to its target. 
"""
import numpy as np 

def RK4(dxdt, x, u, dt): 
    K1 = dt*dxdt(x, u)
    K2 = dt*dxdt(x+K1/2, u)
    K3 = dt*dxdt(x+K2/2, u)
    K4 = dt*dxdt(x+K3, u)
    x1 = x + K1/6+K2/3+K3/3+K4/6
    return np.array(x1)

class one_dim_control(): 
    def __init__(self): 
        self.g = 10 #m/s2 
        self.h_target = 50
        self.h_map = 100
        self.h_bot = 0
        self.dt = 0.05
        self.h = 0 
        self.v = 0
        self.v_min = -10
        self.v_max = 10
        self.t_max = 25
        self.eps = 1e-1

        self.dh_dt = lambda x, u: x[1] # x=[h,v], u=[a]
        self.dv_dt = lambda x, u: u[0]
        self.dxdt = lambda x, u: np.array([self.dh_dt(x, u), self.dv_dt(x, u)])
        
        #self.observation_space = {"n": 3, "low": np.array([self.h_bot-1,self.v_min-1, self.h_target-self.h_map]), "high": np.array([self.h_map+1, self.v_max+1, self.h_target+1])}
        self.observation_space = {"n": 2, "low": np.array([self.h_bot-1,self.v_min-1]), "high": np.array([self.h_map+1, self.v_max+1])}
        self.action_space = {"n": 3} #Where [no a, small a, some a, large a]
        self.actions = np.linspace(0, 20, self.action_space["n"])
        
    def reset(self, eps, rew): 
        self.reward = rew
        self.eps = eps
        self.done = False
        self.h = 0 
        self.v = 0
        self.h_target = np.random.uniform(low=self.h_bot+10, high=self.h_map*0.9)
        self.dh = self.h_target - self.h 
        self.t = 0
        #return np.array([self.h, self.v, self.dh])
        return np.array([self.dh, self.v])
    
    def step(self, action): #Action is boolean values if the veicle is accelerating or not. action = [a, a_not]
        u = [self.actions[action]-self.g]
        x = np.array([self.h, self.v])
        self.h, self.v = RK4(self.dxdt, x, u, self.dt)  

        if self.v > self.v_max: 
            self.v = self.v_max
        elif self.v < self.v_min: 
            self.v = self.v_min

        if self.h < self.h_bot: 
            self.h = 0 
            self.v = 0

        elif self.h > self.h_map: 
            self.h = self.h_map
            self.v = 0
            
        self.dh = self.h_target - self.h 
        self.t += self.dt
        if self.t >= self.t_max: 
            self.done = True
        
        #return np.array([self.h, self.v, self.dh]), self.get_reward(), self.done, "Info"
        return np.array([self.dh, self.v]), self.get_reward(), self.done, "Info"
    
    def get_reward(self): 
        if  self.eps > abs(self.dh):
            return self.reward

        else:
             return -abs(self.dh)*self.dt
        
        

