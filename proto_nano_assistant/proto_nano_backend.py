from flask import Flask, render_template, jsonify
import data

app = Flask(__name__)

@app.route("/")
def dashboard():
    # Send lab inventory and recommendations to frontend
    recommendations = data.get_reorder_recommendations()
    return render_template("dashboard.html", labs=data.labs, recommendations=recommendations)

@app.route("/api/recommendations")
def api_recommendations():
    return jsonify(data.get_reorder_recommendations())

if __name__ == "__main__":
    app.run(debug=True)