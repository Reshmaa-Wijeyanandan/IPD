from flask import Blueprint, request, jsonify
import firebase_admin
from firebase_admin import credentials, messaging

# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_admin.json")
    firebase_admin.initialize_app(cred)

notifications_blueprint = Blueprint('notifications', __name__)  # Define Flask Blueprint

def send_notification(user_id, message):
    """Send push notification for detected emotions"""
    try:
        # Construct Notification Payload
        notification = messaging.Message(
            notification=messaging.Notification(
                title="EmotiGluco - Mood Alert",
                body=message
            ),
            token=user_id  # Assuming user_id is the Firebase Token
        )

        # Send Notification
        response = messaging.send(notification)
        return {"success": True, "message_id": response}

    except Exception as e:
        return {"error": str(e)}

# Flask route to send a notification manually
@notifications_blueprint.route('/send-notification', methods=['POST'])
def send_notification_route():
    data = request.json
    user_id = data.get('user_id')
    message = data.get('message')

    if not user_id or not message:
        return jsonify({"error": "Missing user_id or message"}), 400

    response = send_notification(user_id, message)
    return jsonify(response)
