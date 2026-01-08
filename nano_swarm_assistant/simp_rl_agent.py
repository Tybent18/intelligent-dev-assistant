import numpy as np

class RLAgent:
    def __init__(self, num_labs):
        self.num_labs = num_labs
        self.actions = [0, 2, 4, 6, 8]  # discrete ink units

    def choose_action(self, state):
        # For now: random policy; later upgrade to Q-learning or Deep RL
        return np.random.choice(self.actions, size=self.num_labs)