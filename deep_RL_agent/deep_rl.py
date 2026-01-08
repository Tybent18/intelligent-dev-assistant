import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

class Actor(nn.Module):
    """Outputs actions (ink units)"""
    def __init__(self, input_size, output_size):
        super(Actor, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, 64)
        self.out = nn.Linear(64, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return torch.sigmoid(self.out(x)) * 10  # scale to 0-10 units

class Critic(nn.Module):
    """Estimates value of state-action"""
    def __init__(self, input_size):
        super(Critic, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, 64)
        self.out = nn.Linear(64, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.out(x)

class DDPGAgent:
    def __init__(self, state_dim, action_dim, lr=0.001):
        self.actor = Actor(state_dim, action_dim)
        self.critic = Critic(state_dim + action_dim)
        self.actor_target = Actor(state_dim, action_dim)
        self.critic_target = Critic(state_dim + action_dim)
        self.actor_target.load_state_dict(self.actor.state_dict())
        self.critic_target.load_state_dict(self.critic.state_dict())
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=lr)
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=lr)
        self.gamma = 0.99
        self.tau = 0.01

    def select_action(self, state):
        state = torch.FloatTensor(state)
        return self.actor(state).detach().numpy().astype(int)