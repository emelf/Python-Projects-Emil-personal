# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 11:17:25 2020

@author: Emil Melfald
"""

from first_test import Agent 
import numpy as np 
import gym 
from basic_env_v1 import one_dim_control
import tensorflow as tf
import matplotlib.pyplot as plt

if __name__ == '__main__': 
    tf.compat.v1.disable_eager_execution() 
    #env = gym.make('LunarLander-v2')
    env = one_dim_control()
    lr = 0.001 
    n_games = 500 
    agent = Agent(gamma=0.99, epsilon=1.0, lr=lr, 
                  input_dims=env.observation_space.shape, 
                  n_actions=len(env.action_space), mem_size=1000000, 
                  batch_size=64, epsilon_end=0.01)
    
    agent.load_model("one_dim_control_agent_v2.h5")
    
    observation = env.reset() 
    done = False 
    rewards = []
    sys_state = []
    actions = []
    while not done: 
        action = agent.choose_action(observation)
        observation_, reward, done, info = env.step(action) 
        
        rewards.append(reward)
        sys_state.append(observation)
        actions.append(action)
        
        agent.store_transition(observation, action, reward, observation_, done) 
        observation = observation_ 
        
    h, v, dh = np.array(sys_state).T
    
    fig, ax = plt.subplots(5,1)
    
    ax[0].plot(h)
    ax[0].set_title("Rocket Height")
    ax[1].plot(v)
    ax[1].set_title("Rocket Speed")
    ax[2].plot(np.abs(dh))
    ax[2].set_title("Height Difference to target")
    ax[3].plot(rewards)
    ax[3].set_title("Rewards")
    ax[4].plot(actions)
    ax[4].set_title("Agent Actions")
    fig.tight_layout(h_pad=0.01) 
    fig.set_figheight(7)
    plt.show() 
    
    print(np.sum(rewards))
        
    
        
        