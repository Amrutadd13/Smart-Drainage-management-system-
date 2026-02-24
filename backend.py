from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)

# Store latest data
latest_data = {
    "water_level": 0,
    "risk": "SAFE"
}

EMAIL_ADDRESS = "jpdamruta2024@gmail.com"
EMAIL_PASSWORD = "xtuzfoliukiehdjj""
AUTHORITY_EMAIL = "jpdamruta2024@gmail.com"

def send_email(level):
    msg = MIMEText(f"ALERT!\nWater Level is {level}%.\nImmediate cleaning required.")
    msg['Subject'] = "Drainage Overflow Alert"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = AUTHORITY_EMAIL

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

@app.route("/update", methods=["POST"])
def update():
    global latest_data
    data = request.json
    level = data["water_level"]

    risk = "SAFE"
    if level >= 80:
        risk = "HIGH"
        send_email(level)
    elif level >= 50:
        risk = "WARNING"

    latest_data = {
        "water_level": level,
        "risk": risk
    }

    return jsonify({"status": "received"})

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(latest_data)

if __name__ == "__main__":
    app.run(debug=True)