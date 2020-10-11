import numpy as np 
import matplotlib.pyplot as plt  
from basic_env_v2 import one_dim_control 
from q_agent_v1 import Agent_v1 

env = one_dim_control() 
agent = Agent_v1(LEARNING_RATE=0.1, DISCOUNT=0.95, EPS0=0.5, EPS_DEC_START=0.1, EPS_DEC_STOP=0.8)

agent.prep_agent(env.observation_space['low'], env.observation_space['high'], env.action_space['n'], DISCRETE_OS_SPACE=50, q_init=(-100, -5))
q_table, info, q_tables = agent.train(env, EPISODES=2000, SHOW_EVERY=200)
performance = agent.use_agent(env, render=False)

fig, axes = plt.subplots(4,1)
names = ['avg', 'min', 'max', 'eps']
for ax, name in zip(axes, names): 
    ax.plot(info['ep'], info[name], label=name)
    ax.set_title(name)
    ax.legend()
    ax.grid()

fig.tight_layout(h_pad=-0.2) 
fig.set_figheight(8)
fig.set_figwidth(8)
plt.show()
"""
agent.save_agent("Q_learning_discrete_actions/agent_object")
plt.savefig("Q_learning_discrete_actions/Model_Training_Summary") 
np.save("Q_learning_discrete_actions/q_table", q_table)
np.save("Q_learning_discrete_actions/q_tables", q_tables)"""

