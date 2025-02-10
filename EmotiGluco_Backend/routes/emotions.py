from flask import Blueprint, request, jsonify
from models.emotion_model import detect_emotion

emotions_blueprint = Blueprint('emotions', __name__)

@emotions_blueprint.route('/detect-emotion', methods=['POST'])
def detect_emotion_route():
    """
    API Endpoint to detect emotion from text.
    """
    data = request.json
    text = data.get('text', '')
    user_id = data.get('user_id', '')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    emotion = detect_emotion(text, user_id)
    return jsonify({"emotion": emotion})
