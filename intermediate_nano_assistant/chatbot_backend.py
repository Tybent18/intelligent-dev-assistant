from flask import Flask, render_template, request, jsonify
import data

app = Flask(__name__)

@app.route("/")
def dashboard():
    recommendations = data.get_reorder_recommendations()
    return render_template("dashboard.html", labs=data.labs, recommendations=recommendations)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    response = data.chatbot_response(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)