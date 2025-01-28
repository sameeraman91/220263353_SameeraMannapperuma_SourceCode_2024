from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import pandas as pd
from logic_model import combine_logic
from ml_model import train_model, predict_agents

app = Flask(__name__)
app.secret_key = "supersecretkey"  # For session management

# Mock login credentials
USERNAME = "Hello"
PASSWORD = "World"

# Load dataset
data = pd.read_csv("summary.csv", parse_dates=["date"], dayfirst=True)

# Pre-train the ML model for each day type
day_types = data["day_type"].unique()
models = {day_type: train_model(day_type, data) for day_type in day_types}


@app.route("/")
def login():
    if "logged_in" in session and session["logged_in"]:
        return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def handle_login():
    username = request.form["username"]
    password = request.form["password"]

    if username == USERNAME and password == PASSWORD:
        session["logged_in"] = True
        return redirect(url_for("index"))
    else:
        return render_template("login.html", error="Invalid credentials")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))


@app.route("/home")
def index():
    if "logged_in" not in session or not session["logged_in"]:
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route("/generate_report", methods=["POST"])
def generate_report():
    request_data = request.get_json()
    selected_date = request_data.get("selected_date")

    if not selected_date:
        return jsonify({"error": "No date provided"}), 400

    try:
        selected_rows = combine_logic(selected_date)
        day_type = selected_rows["day_type"].iloc[0]
        model = models[day_type]
        agent_predictions = predict_agents(selected_rows, model)

        report = {
            "total_calls": selected_rows["total_calls_for_date"].mean(),
            "missed_calls": selected_rows["missed_call_for_day"].mean(),
            "shift_calls": selected_rows[
                [
                    "S1_english_calls", "S1_sinhala_calls", "S1_tamil_calls",
                    "S2_english_calls", "S2_sinhala_calls", "S2_tamil_calls",
                    "S3_english_calls", "S3_sinhala_calls", "S3_tamil_calls",
                ]
            ].mean().to_dict(),
            "agent_allocations": agent_predictions.tolist(),
        }
        return jsonify(report)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Added: API endpoint for login form (to work with updated JavaScript)
@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == USERNAME and password == PASSWORD:
        session["logged_in"] = True
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


if __name__ == "__main__":
    app.run(debug=True)
