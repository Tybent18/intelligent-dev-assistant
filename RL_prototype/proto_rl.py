import numpy as np

# Simulated Labs
labs = ["LabA", "LabB", "LabC"]
num_labs = len(labs)

# Simulated usage per timestep (random for example)
def simulate_usage():
    return np.random.randint(1, 6, size=num_labs)

# Environment class
class NanoInkEnv:
    def __init__(self):
        self.stock = np.array([20, 15, 18], dtype=int)
        self.max_stock = 30
        self.usage_history = []

    def step(self, action):
        """
        action: array of ink units to send to each lab
        Returns: next_state, reward
        """
        # Add delivered ink
        self.stock += action

        # Simulate usage
        usage = simulate_usage()
        self.stock -= usage
        self.usage_history.append(usage)

        # Reward: penalize shortages, penalize excess
        reward = 0
        for s in self.stock:
            if s < 0:
                reward -= 10  # shortage
            elif s > self.max_stock:
                reward -= (s - self.max_stock)  # excess
        # Optional: small reward for balanced stock
        reward += 5 * np.sum((self.stock >= 5) & (self.stock <= self.max_stock))
        
        # Clip negative stock to zero
        self.stock = np.clip(self.stock, 0, self.max_stock)
        
        return self.stock.copy(), reward

    def reset(self):
        self.stock = np.array([20, 15, 18], dtype=int)
        self.usage_history = []
        return self.stock.copy()

# Simple Q-learning agent
class QAgent:
    def __init__(self, num_labs):
        self.q_table = {}  # State-action mapping
        self.num_labs = num_labs
        self.actions = [0, 2, 4, 6, 8]  # discrete ink units to send

    def choose_action(self, state):
        # For simplicity, random action
        return np.random.choice(self.actions, size=self.num_labs)

# Training loop
env = NanoInkEnv()
agent = QAgent(num_labs)

episodes = 50
for ep in range(episodes):
    state = env.reset()
    total_reward = 0
    for t in range(10):  # 10 timesteps per episode
        action = agent.choose_action(state)
        next_state, reward = env.step(action)
        total_reward += reward
        state = next_state
    print(f"Episode {ep+1} total reward: {total_reward}, final stock: {state}")