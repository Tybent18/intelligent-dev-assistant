import numpy as np
import gym
from gym import spaces

class NanoInkEnvRL(gym.Env):
    """Gym environment for nano ink distribution with history"""
    def __init__(self, history_days=30):
        super().__init__()
        self.num_labs = 3
        self.max_stock = 30
        self.history_days = history_days
        self.action_space = spaces.Box(low=0, high=10, shape=(self.num_labs,), dtype=np.int32)
        self.observation_space = spaces.Box(low=0, high=self.max_stock, shape=(self.num_labs + self.num_labs*history_days,), dtype=np.float32)
        self.reset()

    def reset(self):
        # Current stock
        self.stock = np.random.randint(10, 20, size=self.num_labs)
        # Historical usage (rows = labs, columns = days)
        self.history = np.random.randint(1, 6, size=(self.num_labs, self.history_days))
        return self.get_state()

    def get_state(self):
        return np.concatenate([self.stock, self.history.flatten()])

    def step(self, action):
        action = np.clip(action, 0, 10).astype(int)
        self.stock += action
        # Simulate today’s usage
        usage = np.random.randint(1, 6, size=self.num_labs)
        self.stock -= usage
        # Update history
        self.history = np.roll(self.history, -1, axis=1)
        self.history[:, -1] = usage

        # Reward: penalize shortages heavily
        reward = 0
        for s in self.stock:
            if s < 5: reward -= 10
            elif s > self.max_stock: reward -= (s - self.max_stock)
        reward += 5 * np.sum((self.stock >= 5) & (self.stock <= self.max_stock))
        self.stock = np.clip(self.stock, 0, self.max_stock)
        done = False
        return self.get_state(), reward, done, {}

    def render(self):
        print("Stock:", self.stock)