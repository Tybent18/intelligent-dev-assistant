from flask import Flask, render_template, request, jsonify
import data
from agent import RLAgent

app = Flask(__name__)
env = data.NanoInkEnv()
agent = RLAgent(data.num_labs)

@app.route("/")
def dashboard():
    state = env.get_state()
    return render_template("dashboard.html", labs=data.labs, stock=state)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    response = data.chatbot_response(user_message)
    return jsonify({"response": response})

@app.route("/recommend", methods=["GET"])
def recommend():
    state = env.get_state()
    action = agent.choose_action(state)
    next_state, reward = env.step(action)
    return jsonify({
        "action": action.tolist(),
        "predicted_stock": next_state.tolist(),
        "reward": reward
    })

if __name__ == "__main__":
    app.run(debug=True)