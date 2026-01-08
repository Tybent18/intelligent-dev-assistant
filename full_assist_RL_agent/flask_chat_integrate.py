from flask import Flask, request, render_template, jsonify
import torch
from data import NanoInkEnvRL
from agent import DDPGAgent
from predictor import DemandPredictor
import numpy as np

app = Flask(__name__)

env = NanoInkEnvRL()
agent = DDPGAgent(state_dim=env.observation_space.shape[0], action_dim=env.action_space.shape[0])
predictor = DemandPredictor(num_labs=env.num_labs, history_days=env.history_days)

current_state = env.reset()
last_action = [0]*env.num_labs

@app.route('/')
def dashboard():
    return render_template("dashboard.html", stock=env.stock, action=last_action)

@app.route('/step', methods=['POST'])
def step():
    global current_state, last_action
    # Agent predicts next action
    last_action = agent.select_action(current_state)
    next_state, reward, done, _ = env.step(last_action)
    current_state = next_state
    return jsonify(stock=env.stock.tolist(), action=last_action.tolist(), reward=reward)

@app.route('/query', methods=['POST'])
def query():
    text = request.json.get("query").lower()
    # Simple rules for now
    if "shortage" in text or "run out" in text:
        shortage_labs = [f"Lab{i+1}" for i,s in enumerate(env.stock) if s < 5]
        answer = f"Labs likely to run out: {', '.join(shortage_labs)}" if shortage_labs else "No labs are at risk"
    elif "suggest" in text:
        answer = f"Suggested shipments: {last_action}"
    else:
        answer = "I can suggest shipments or report potential shortages"
    return jsonify(answer=answer)

if __name__ == "__main__":
    app.run(debug=True)