import numpy as np 
import time 
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from tensorflow import keras

class ReplayBuffer(): 
    def __init__(self, max_size, input_dim): 
        self.mem_size = max_size
        self.mem_cntr = 0 
        
        #These are the agent memories that keep track of what actions are good and not good. 
        #The memories will start filling up as the agent learns, and when memory is full ... 
        #the oldest memory will be replaced for new ones. 
        
        #State memory: Keeps track of what the agent sees at each time step, "initial memory"
        self.state_memory = np.zeros((self.mem_size, *input_dim), dtype=np.float32)
        #State transision memory - A memory where new data coming in
        self.new_state_memory = np.zeros((self.mem_size, *input_dim), dtype=np.float32)
        #Memory for actions
        self.action_memory = np.zeros(self.mem_size, dtype=np.int32)
        self.reward_memory = np.zeros(self.mem_size, dtype=np.float32)
        #Keeping track of our "done"-flags
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.int32)
        
    def store_transition(self, state, action, reward, state_, done): 
        #Find index of the first unoccupied memory
        index = self.mem_cntr % self.mem_size 
        self.state_memory[index] = state
        self.new_state_memory[index] = state_
        self.reward_memory[index] = reward 
        self.action_memory[index] = action 
        self.terminal_memory[index] = 1 - int(done) 
        self.mem_cntr += 1 
    
    def sample_buffer(self, batch_size): 
        #When agent is learning, only used stored memory, and not ... 
        #unused memory, because thats a lot of 0's 
        max_mem = min(self.mem_cntr, self.mem_size)
        #Once memory is selected, it gets removed
        batch = np.random.choice(max_mem, batch_size, replace=False)
        
        states = self.state_memory[batch] 
        states_ = self.new_state_memory[batch]
        rewards = self.reward_memory[batch] 
        actions = self.action_memory[batch] 
        terminal = self.terminal_memory[batch] 
        
        return states, actions, rewards, states_, terminal
    
    
def build_dqn(lr, n_actions, input_dims, fc1_dims, fc2_dims): 
    model = keras.Sequential([
        keras.layers.Dense(fc1_dims, activation='relu'), 
        keras.layers.Dense(fc2_dims, activation='relu'), 
        keras.layers.Dense(n_actions, activation=None)])
    model.compile(optimizer=Adam(learning_rate=lr), loss='mse') 
    return model  

#Agent class: 
class Agent(): 
    def __init__(self, lr, gamma, n_actions, epsilon, batch_size, 
                 input_dims, epsilon_dec=1e-4, epsilon_end=0.01, 
                 mem_size=1000000, fname='dqn_model.h5'): 
        self.action_space = [i for i in range(n_actions)] 
        self.gamma = gamma 
        self.epsilon = epsilon 
        self.eps_min = epsilon_end 
        self.eps_dec = epsilon_dec
        self.batch_size = batch_size 
        self.model_file = fname 
        self.memory = ReplayBuffer(mem_size, input_dims)
        self.q_eval = build_dqn(lr, n_actions, input_dims, 64, 64) 
        
    def store_transition(self, state, action, reward, new_state, done): 
        self.memory.store_transition(state, action, reward, new_state, done) 
        
    def choose_action(self, observation): 
        if np.random.random() < self.epsilon: #Causes the agent to choose random actions at the beginning of training
            action = np.random.choice(self.action_space)
        else: 
            state = np.array([observation])
            action = self.q_eval.predict(state) 
            action = np.argmax(action) 
            
        return action 
    
    def learn(self): 
        if self.memory.mem_cntr < self.batch_size: 
            return 
        
        states, actions, rewards, states_, dones = \
            self.memory.sample_buffer(self.batch_size)
            
        q_eval = self.q_eval.predict(states)
        q_next = self.q_eval.predict(states_)
        
        q_target = np.copy(q_eval) 
        batch_index = np.arange(self.batch_size, dtype=np.int32)
        q_target[batch_index, actions] = rewards + \
            self.gamma + np.max(q_next, axis=1)*dones
            
        self.q_eval.train_on_batch(states, q_target)
        self.epsilon = self.epsilon - self.eps_dec if self.epsilon > \
            self.eps_min else self.eps_min 
            
    def save_model(self, filename): 
        self.q_eval.save(filename)
        
    def load_model(self, filename): 
        self.q_eval = load_model(filename)          
            
    
        