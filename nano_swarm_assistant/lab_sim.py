import numpy as np

labs = ["LabA", "LabB", "LabC"]
num_labs = len(labs)

# Initial stock per lab
init_stock = np.array([20, 15, 18], dtype=int)
max_stock = 30

class NanoInkEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.stock = init_stock.copy()
        self.usage_history = []
        return self.stock.copy()

    def step(self, action):
        """Update stock based on AI action and simulate usage."""
        self.stock += action  # delivered ink
        usage = np.random.randint(1, 6, size=num_labs)
        self.stock -= usage
        self.usage_history.append(usage)

        # Reward: penalize shortages, penalize excess
        reward = 0
        for s in self.stock:
            if s < 0: reward -= 10
            elif s > max_stock: reward -= (s - max_stock)
        reward += 5 * np.sum((self.stock >= 5) & (self.stock <= max_stock))

        # Clip stock to feasible range
        self.stock = np.clip(self.stock, 0, max_stock)
        return self.stock.copy(), reward

    def get_state(self):
        return self.stock.copy()

# Simple chatbot logic for dashboard
def chatbot_response(message):
    message = message.lower()
    if "which labs need ink" in message:
        recs = {}
        for idx, s in enumerate(init_stock):
            if s < 10:
                recs[labs[idx]] = 10 - s
        if not recs:
            return "All labs have sufficient ink."
        return "Labs needing ink: " + ", ".join(f"{lab} ({amt} units)" for lab, amt in recs.items())
    elif "stock of" in message:
        for lab in labs:
            if lab.lower() in message:
                return f"{lab} stock: {init_stock[labs.index(lab)]}"
        return "Lab not found."
    else:
        return "Ask me about lab stock or which labs need ink."