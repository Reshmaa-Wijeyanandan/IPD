from flask import Blueprint, request, jsonify
from database import db
from datetime import datetime

glucose_blueprint = Blueprint('glucose', __name__)  # Ensure it's registered

#  **Log Glucose Level**
@glucose_blueprint.route('/log-glucose', methods=['POST'])
def log_glucose():
    print(" Glucose route accessed!")  # Debug log

    data = request.json
    if not data:
        print(" No data received")
        return jsonify({"error": "No data received"}), 400

    user_id = data.get('user_id')
    glucose_level = data.get('glucose_level')
    date = data.get('date')  #  Get date from frontend
    time = data.get('time')  #  Get time from frontend

    if not user_id or not glucose_level or not date or not time:
        print(" Missing required fields")
        return jsonify({"error": "Missing required fields"}), 400

    #  Store in MongoDB
    db.glucose_logs.insert_one({
        "user_id": user_id,
        "glucose_level": glucose_level,
        "date": date,  #  Store date separately
        "time": time,  #  Store time separately
        "timestamp": datetime.utcnow()  #  Also store full timestamp for reference
    })

    print(" Glucose log saved!")
    return jsonify({"message": "Glucose log recorded"}), 201

# 🔹 **Fetch Glucose History**
@glucose_blueprint.route('/get-glucose', methods=['GET'])
def get_glucose():
    user_id = request.args.get("user_id")

    if not user_id:
        print(" Missing user_id in request")
        return jsonify({"error": "Missing user_id"}), 400

    glucose_logs = list(db.glucose_logs.find({"user_id": user_id}, {"_id": 0}))  #  Exclude MongoDB `_id` field

    print(f" Found {len(glucose_logs)} glucose entries for user {user_id}")
    return jsonify({"glucose_logs": glucose_logs}), 200
