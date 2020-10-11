import numpy as np 
import matplotlib.pyplot as plt
from numpy.random import random
import pickle

#This agent is meant to act and observe outcome of environment in the same action.
#This means that agents cannot do actions simotaniously with this agent class. 

class Agent_v2: 
    def __init__(self, obs_space_low, obs_space_high, action_space, DISCRETE_OS_SPACE=20, q_init=(-2,0)): 
        """Prepares the agent to an environment. To avoid confusion and too much generalization, this function needs the observation spaces directly."""
        self.obs_space_low = obs_space_low #List of low limits
        self.obs_space_high = obs_space_high #List of high limits from observation space
        self.action_space = action_space #An integer of how many actions the agent will have
        self.DISCRETE_OS_SIZE = [DISCRETE_OS_SPACE]*len(self.obs_space_low) 
        self.discrete_os_win_size = (obs_space_high-obs_space_low) / self.DISCRETE_OS_SIZE
        self.q_table = np.random.uniform(low=q_init[0], high=q_init[1], size=(self.DISCRETE_OS_SIZE + [action_space]))

        self.metrics = {"Games_won": 0, "Games_lost": 0, "Rewards": [], "Game_points": [], "Epsilon":[]}
        self.init = True

    def update_agent(self, LEARNING_RATE=0.1, DISCOUNT=0.9, EPS0=0.5, EPS_DEC=1e-3, EPS_MIN=0): 
        self.lr = LEARNING_RATE #How fast the weights is updated
        self.discount = DISCOUNT
        self.epsilon0 = EPS0 #High epsilon means high exploration rate
        self.epsilon = EPS0
        self.EPS_DEC = EPS_DEC 
        self.EPS_MIN = EPS_MIN

    def get_discrete_state(self, state): 
        #Converts from float to the index value of what observation the agent sees, 
        #based on its observational limits
        
        #Check for states out of observational bounds: 
        for low, high, state_in in zip(self.obs_space_low, self.obs_space_high, state): 
            if state_in <= low: 
                state_in = low 
            elif state_in >= high: 
                state_in = high-1
        #Converts from float to integer index values of observation
        discrete_state = (state-self.obs_space_low)/self.discrete_os_win_size
        return tuple(discrete_state.astype(np.int)) 

    def update_epsilon(self): 
        self.epsilon -= self.EPS_DEC
        if self.epsilon <= self.EPS_MIN: 
            self.epsilon = self.EPS_MIN

    def act(self, env):
        discrete_state = self.get_discrete_state(env.get_state(self))
        action = self.find_action(discrete_state)
        
        new_state, reward, _ = env.step(action, self) 
        new_discrete_state = self.get_discrete_state(new_state) 
        self.update_q_value(discrete_state, new_discrete_state, action, reward)

    def find_action(self, discrete_state): 
        if random() > self.epsilon: 
            action = np.argmax(self.q_table[discrete_state])
        else: 
            action = np.random.randint(0, self.action_space)
        return action #Returns an integer for which action index is chosen by the agent

    def update_q_value(self, discrete_state, new_discrete_state, action, reward): 
        max_future_q = np.max(self.q_table[new_discrete_state])
        current_q = self.q_table[discrete_state+(action, )]
        new_q = (1-self.lr)*current_q + self.lr*(reward+self.discount*max_future_q)
        self.q_table[discrete_state+(action,)] = new_q

    def save_agent(self, filename): 
        pickle.dump(self, open(filename+".p", "wb"))



