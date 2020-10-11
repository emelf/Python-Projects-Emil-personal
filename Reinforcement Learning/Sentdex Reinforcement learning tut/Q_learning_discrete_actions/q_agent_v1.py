import numpy as np 
import matplotlib.pyplot as plt
from numpy.random import random
import pickle


class Agent_v1: 
    def __init__(self, LEARNING_RATE=0.1, DISCOUNT=0.9, EPS0=0.5, EPS_DEC_START=0.1, EPS_DEC_STOP=0.8, player=0): 
        self.lr = LEARNING_RATE #How fast the weights is updated
        self.discount = DISCOUNT
        self.epsilon0 = EPS0 #High epsilon means high exploration rate
        self.START_EPSILON_DECAYING = EPS_DEC_START
        self.END_EPSILON_DECAYING = EPS_DEC_STOP #Epsilon stop decaying after half the episodes
        #self.epsilon_decay_val = self.epsilon0/(self.END_EPSILON_DECAYING-self.START_EPSILON_DECAYING)
        self.player = player

    def update_agent(self, LEARNING_RATE=0.1, DISCOUNT=0.9, EPS0=0.5, EPS_DEC_START=0.1, EPS_DEC_STOP=0.8): 
        self.lr = LEARNING_RATE #How fast the weights is updated
        self.discount = DISCOUNT
        self.epsilon0 = EPS0 #High epsilon means high exploration rate
        self.START_EPSILON_DECAYING = EPS_DEC_START
        self.END_EPSILON_DECAYING = EPS_DEC_STOP #Epsilon stop decaying after half the episodes
        self.epsilon_decay_val = self.epsilon0/(self.END_EPSILON_DECAYING-self.START_EPSILON_DECAYING)

    def get_discrete_state(self, state): 
        discrete_state = (state-self.obs_space_low)/self.discrete_os_win_size
        return tuple(discrete_state.astype(np.int)) 

    def prep_agent(self, obs_space_low, obs_space_high, action_space, DISCRETE_OS_SPACE=20, q_init=(-2,0)):
        """Prepares the agent to an environment. To avoid confusion and too much generalization, this function needs the observation spaces directly."""
        self.obs_space_low = obs_space_low
        self.obs_space_high = obs_space_high
        self.action_space = action_space
        self.DISCRETE_OS_SIZE = [DISCRETE_OS_SPACE]*len(obs_space_low) 
        self.discrete_os_win_size = (obs_space_high-obs_space_low) / self.DISCRETE_OS_SIZE
        self.q_table = np.random.uniform(low=q_init[0], high=q_init[1], size=(self.DISCRETE_OS_SIZE + [action_space]))
        self.q_tables = [self.q_table]
        self.aggr_ep_rewards = {'ep': [], 'avg': [], 'min': [], 'max': [], 'eps': []}

    def train(self, env, EPISODES=2000, SHOW_EVERY=500, SAVE_EVERY=50):
        epsilon = self.epsilon0 #High epsilon means high exploration rate
        START_EPSILON_DECAYING = int(self.START_EPSILON_DECAYING*EPISODES)
        END_EPSILON_DECAYING = int(self.END_EPSILON_DECAYING*EPISODES)
        epsilon_decay_val = self.epsilon0/(END_EPSILON_DECAYING-START_EPSILON_DECAYING)
        scores = []

        discrete_state = self.get_discrete_state(env.reset())

        for episode in range(EPISODES): 
            render = self.render_episode(episode, SHOW_EVERY)
            done = False 
            state = env.reset() 
            discrete_state = self.get_discrete_state(state)
            score = 0

            while not done: 
                action = self.find_action(discrete_state, epsilon)
                new_state, reward, done, _ = env.step(action) 
                score += reward
                new_discrete_state = self.get_discrete_state(new_state) 
                if not done: 
                    self.update_q_value(discrete_state, new_discrete_state, action, reward)
                discrete_state = new_discrete_state
                if render: 
                    try: 
                        env.render() 
                    except: 
                        pass     
            scores.append(score)

            if render:
                print("Episode: {}, Current Score: {}, Epsilon = {}. Average Score: {}, Min Score: {}, Max Score: {}.".format(
                        episode, round(score,2), round(epsilon,3), round(np.mean(scores[-SHOW_EVERY:]),2), 
                        round(np.min(scores[-SHOW_EVERY:]),2), round(np.max(scores[-SHOW_EVERY:]),2)))
                
            epsilon = self.decay_epsilon(START_EPSILON_DECAYING, END_EPSILON_DECAYING, epsilon_decay_val, episode, epsilon) 

            if episode % SAVE_EVERY == 0: 
                self.aggr_ep_rewards['ep'].append(episode)
                self.aggr_ep_rewards['avg'].append(np.average(scores[-SAVE_EVERY:]))
                self.aggr_ep_rewards['min'].append(np.min(scores[-SAVE_EVERY:]))
                self.aggr_ep_rewards['max'].append(np.max(scores[-SAVE_EVERY:]))
                self.aggr_ep_rewards['eps'].append(epsilon)
                self.q_tables.append(self.q_table)

        return self.q_table, self.aggr_ep_rewards, self.q_tables

    def render_episode(self, episode, SHOW_EVERY): 
        if episode % SHOW_EVERY == 0:
            render = True 
        else: 
            render = False
        return render

    def find_action(self, discrete_state, epsilon): 
        if random() > epsilon: 
            action = np.argmax(self.q_table[discrete_state])
        else: 
            action = np.random.randint(0, self.action_space)
        return action

    def update_q_value(self, discrete_state, new_discrete_state, action, reward): 
        max_future_q = np.max(self.q_table[new_discrete_state])
        current_q = self.q_table[discrete_state+(action, )]
        new_q = (1-self.lr)*current_q + self.lr*(reward+self.discount*max_future_q)
        self.q_table[discrete_state+(action,)] = new_q

    def decay_epsilon(self, SED, EED, EDV, episode, epsilon): 
        if EED >= episode >= SED: 
            epsilon -= EDV 
        if epsilon < 0: 
            epsilon = 0
        return epsilon

    def use_agent(self, env, render=False): 
        done = False 
        state = env.reset() 
        discrete_state = self.get_discrete_state(state)
        agg_agent = {'frame': [], 'actions': [], 'states': [], 'rewards': []}
        frame = 0
        score = 0
        while not done: 
            frame += 1
            action = np.argmax(self.q_table[discrete_state])
            new_state, reward, done, _ = env.step(action) 
            score += reward
            new_discrete_state = self.get_discrete_state(new_state) 
            agg_agent['frame'].append(frame)
            agg_agent['actions'].append(action)
            agg_agent['states'].append(new_state)
            agg_agent['rewards'].append(reward)
            if not done: 
                self.update_q_value(discrete_state, new_discrete_state, action, reward)
            discrete_state = new_discrete_state
            if render: 
                env.render() 
        agg_agent['score'] = score 
        return agg_agent

    def save_agent(self, filename): 
        pickle.dump(self, open(filename+".p", "wb"))

