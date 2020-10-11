import numpy as np 
import matplotlib.pyplot as plt  
import gym 
from basic_env_v1 import one_dim_control 

def get_discrete_state(state): 
    discrete_state = (state-env.observation_space["low"])/discrete_os_win_size
    return tuple(discrete_state.astype(np.int))


def plot_one_sim(q_table, eps):
    states = [env.reset(eps, 10)]
    discrete_state = get_discrete_state(states[0])
    rewards = [] 
    actions = []

    done = False 
    while not done: 
        action = np.argmax(q_table[discrete_state])
        actions.append(action)
        new_state, reward, done, _ = env.step(action) 
        states.append(new_state)
        rewards.append(reward) 
        discrete_state = get_discrete_state(new_state)

    states = np.array(states).T 
    actions = np.array(actions)

    fig, ax = plt.subplots(4,1)
    ax[0].plot(states[0])
    ax[0].set_title("Position")
    ax[0].grid()

    ax[1].plot(states[1])
    ax[1].set_title("Velocity")
    ax[1].grid()

    ax[2].plot(rewards)
    ax[2].set_title("Reward")
    ax[2].grid()

    ax[3].plot(actions)
    ax[3].set_title("Actions")
    ax[3].grid()

    fig.tight_layout(h_pad=-0.2)
    plt.show()

def train_qtable(q_table, episodes, epsilon0, lr, eps, rew):
    EPISODES = episodes 
    LEARNING_RATE = lr #How fast the weights is updated
    epsilon = epsilon0 #High epsilon means high exploration rate
    START_EPSILON_DECAYING = EPISODES//5
    END_EPSILON_DECAYING = 4*EPISODES//5 #Epsilon shour stop decaying after half the episodes
    epsilon_decay_val = epsilon/(END_EPSILON_DECAYING-START_EPSILON_DECAYING)

    discrete_state = get_discrete_state(env.reset(eps, rew))
    scores = []

    for episode in range(EPISODES): 
        if episode % SHOW_EVERY == 0:
            render = True 
        else: 
            render = False
        done = False 
        frame = 0
        state = env.reset(eps, rew) 
        discrete_state = get_discrete_state(state)
        frames = []
        score = 0
        while not done: 
            frame += 1
            if np.random.random() > epsilon: 
                action = np.argmax(q_table[discrete_state])
            else: 
                action = np.random.randint(0, env.action_space["n"])
            new_state, reward, done, _ = env.step(action) 
            score += reward
            new_discrete_state = get_discrete_state(new_state) 
            if not done: 
                max_future_q = np.max(q_table[new_discrete_state])
                current_q = q_table[discrete_state+(action, )]

                new_q = (1-LEARNING_RATE)*current_q + LEARNING_RATE*(reward+DISCOUNT*max_future_q)
                q_table[discrete_state+(action,)] = new_q
            frames.append(frame)
            discrete_state = new_discrete_state
        scores.append(score)
        if episode % SHOW_EVERY == 0:
            print("The episode is {}. The score is {}. Epsilon = {}. Average Score last 100: {}.".format(
                    episode, round(score,2), round(epsilon,3), round(np.mean(scores[-100:]),2)))
        if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING: 
            epsilon -= epsilon_decay_val
    print("The episode is {}. The score is {}. Epsilon = {}. Average Score last 100: {}.".format(
                    episode, round(score,2), round(epsilon,3), round(np.mean(scores[-100:]),2)))

    return q_table



#env = gym.make("MountainCar-v0")
env = one_dim_control() 
DISCOUNT = 0.9
SHOW_EVERY = 500 #Shows whats up every 2000 episodes
SHOW_EPS = 1000
#How many discrete observation values?
DISCRETE_OS_SIZE = [60]*len(env.observation_space["high"]) 
discrete_os_win_size = (env.observation_space["high"]-env.observation_space["low"]) / DISCRETE_OS_SIZE
q_table = np.random.uniform(low=-2, high=0, 
                            size=(DISCRETE_OS_SIZE + [env.action_space["n"]]))



#Program: 
plot_one_sim(q_table, eps=10) #How it did initially
q_table1 = train_qtable(q_table, episodes=10000, epsilon0=0.5, lr=0.1, eps=5, rew=10)
plot_one_sim(q_table1, eps=5) #After first training 
q_table2 = train_qtable(q_table1, episodes=5000, epsilon0=0.2, lr=0.05, eps=1, rew=10)
np.save("q_table1.npy", q_table2)
plot_one_sim(q_table2, eps=1)


