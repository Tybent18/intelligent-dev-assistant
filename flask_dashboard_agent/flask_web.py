from flask import Flask, render_template, request, jsonify
from data import NanoInkEnvRL
from agent import DDPGAgent
import torch
import threading

app = Flask(__name__)

# Initialize environment & agent
env = NanoInkEnvRL()
agent = DDPGAgent(state_dim=env.observation_space.shape[0],
                  action_dim=env.action_space.shape[0])

current_stock = env.reset()
last_action = [0] * env.observation_space.shape[0]

# Lock for thread-safe updates
lock = threading.Lock()

@app.route('/')
def dashboard():
    return render_template('dashboard.html', stock=current_stock, action=last_action)

@app.route('/step', methods=['POST'])
def step_env():
    global current_stock, last_action
    with lock:
        # Agent decides action
        last_action = agent.select_action(current_stock)
        current_stock, reward, done, _ = env.step(last_action)
    return jsonify(stock=current_stock.tolist(), action=last_action.tolist(), reward=reward)

if __name__ == '__main__':
    app.run(debug=True)