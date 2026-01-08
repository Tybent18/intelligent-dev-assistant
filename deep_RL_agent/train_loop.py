import torch
from data import NanoInkEnvRL
from agent import DDPGAgent

env = NanoInkEnvRL()
agent = DDPGAgent(state_dim=env.observation_space.shape[0],
                  action_dim=env.action_space.shape[0])

episodes = 500
for ep in range(episodes):
    state = env.reset()
    ep_reward = 0
    for t in range(50):
        action = agent.select_action(state)
        next_state, reward, done, _ = env.step(action)
        ep_reward += reward
        state = next_state
    if ep % 10 == 0:
        print(f"Episode {ep}, Reward: {ep_reward}")