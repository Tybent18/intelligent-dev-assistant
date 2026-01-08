import torch
import torch.nn as nn
import torch.optim as optim

class DemandPredictor(nn.Module):
    """Predicts next day usage per lab based on history"""
    def __init__(self, num_labs, history_days):
        super().__init__()
        self.fc1 = nn.Linear(num_labs*history_days, 64)
        self.fc2 = nn.Linear(64, 32)
        self.out = nn.Linear(32, num_labs)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.out(x)  # predicted usage next day