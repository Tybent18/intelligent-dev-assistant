import numpy as np
import gym
from gym import spaces

labs = ["LabA", "LabB", "LabC"]
num_labs = len(labs)
max_stock = 30
min_stock = 0

class NanoInkEnvRL(gym.Env):
    """Gym-style environment for Nano Ink distribution"""
    def __init__(self):
        super(NanoInkEnvRL, self).__init__()
        self.action_space = spaces.Box(low=0, high=10, shape=(num_labs,), dtype=np.int32)  # units of ink per lab
        self.observation_space = spaces.Box(low=0, high=max_stock, shape=(num_labs,), dtype=np.int32)
        self.reset()

    def reset(self):
        self.stock = np.random.randint(10, 20, size=num_labs)
        return self.stock.copy()

    def step(self, action):
        action = np.clip(action, 0, 10).astype(int)
        self.stock += action  # delivered ink
        usage = np.random.randint(1, 6, size=num_labs)
        self.stock -= usage

        # Reward: penalize shortages heavily, overstock lightly
        reward = 0
        for s in self.stock:
            if s < 5:
                reward -= 10
            elif s > max_stock:
                reward -= (s - max_stock)
        reward += 5 * np.sum((self.stock >= 5) & (self.stock <= max_stock))

        # Clip stock
        self.stock = np.clip(self.stock, 0, max_stock)
        done = False  # can implement episode length later
        return self.stock.copy(), reward, done, {}

    def render(self):
        print("Current stock:", self.stock)