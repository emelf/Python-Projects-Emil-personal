import numpy as np 
import matplotlib.pyplot as plt  
import gym 
from basic_env_v1 import one_dim_control 

def discretize_states(state, win_size, s_min): #My function
    new_state = [] 
    for s, s_m, w_s in zip(state, s_min, win_size): 
        j = 0
        while s > j*w_s+s_m:
            j += 1
        new_state.append((j-1)*w_s+s_m)
    return new_state

def get_discrete_state(state): 
    discrete_state = (state-env.observation_space.low)/discrete_os_win_size
    return tuple(discrete_state.astype(np.int))


env = gym.make("MountainCar-v0")

LEARNING_RATE = 0.1 #How fast the weights is updated
DISCOUNT = 0.95 #How important do we find future actions, val betw 0 and 1
EPISODES = 5000 
SHOW_EVERY = 100 #Shows whats up every 2000 episodes
SHOW_EPS = 1000
#How many discrete observation values?
DISCRETE_OS_SIZE = [20]*len(env.observation_space.high) 
#This is done to be able to fit in action vs observations in memory 
#Here we get 20 "buckets" of different observation numbers

ep_rewards = []
aggr_ep_rewards = {'ep': [], 'avg': [], 'min': [], 'max': []}

discrete_os_win_size = (env.observation_space.high-env.observation_space.low) / DISCRETE_OS_SIZE


#Creating q-table for the agent 
#The q table is the agents memory, which maps actions to observations and rewards. 
q_table = np.random.uniform(low=-2, high=0, 
                            size=(DISCRETE_OS_SIZE + [env.action_space.n]))
epsilon = 0.5 #High epsilon means high exploration rate
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = EPISODES//2 #Epsilon shour stop decaying after half the episodes

epsilon_decay_val = epsilon/(END_EPSILON_DECAYING-START_EPSILON_DECAYING)

discrete_state = get_discrete_state(env.reset())
for episode in range(EPISODES): 
    episode_reward = 0
    if episode % SHOW_EVERY == 0:
        render = True 
    else: 
        render = False


    done = False 
    frame = 0
    env.reset() 
    frames = []
    while not done: 
        frame += 1
        if np.random.random() > epsilon: 
            action = np.argmax(q_table[discrete_state])
        else: 
            action = np.random.randint(0, env.action_space.n)
        new_state, reward, done, _ = env.step(action) 
        episode_reward += reward
        new_discrete_state = get_discrete_state(new_state) 
        if render:
            pass
            #env.render()  
        if not done: 
            max_future_q = np.max(q_table[new_discrete_state])
            current_q = q_table[discrete_state+(action, )]

            new_q = (1-LEARNING_RATE)*current_q + LEARNING_RATE*(reward+DISCOUNT*max_future_q)
            q_table[discrete_state+(action,)] = new_q
        elif new_state[0] >= env.goal_position: 
            q_table[discrete_state+(action,)] = 0
            #print("He made it! The episode is {}. It took {} frames. Epsilon = {}".format(
            #     episode, frame, round(epsilon,3)))
        frames.append(frame)
        discrete_state = new_discrete_state
    ep_rewards.append(episode_reward) 
    if not episode % SHOW_EVERY: #Same as if episode % SHOW_EVERY == 0:
        average_reward = np.average(ep_rewards[-SHOW_EVERY:])
        aggr_ep_rewards['ep'].append(episode)
        aggr_ep_rewards['avg'].append(np.average(ep_rewards[-SHOW_EVERY:]))
        aggr_ep_rewards['min'].append(np.min(ep_rewards[-SHOW_EVERY:]))
        aggr_ep_rewards['max'].append(np.max(ep_rewards[-SHOW_EVERY:]))
        print("Episode:{}, avg: {}, min: {}, max: {}".format(
              episode, np.average(ep_rewards[-SHOW_EVERY:]), 
              np.min(ep_rewards[-SHOW_EVERY:]), np.max(ep_rewards[-SHOW_EVERY:])
        ))
    if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING: 
        epsilon -= epsilon_decay_val
env.close()


plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['avg'], label='avg')
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['min'], label='min')
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['max'], label='max')
plt.legend()
