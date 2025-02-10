import requests
import time
from flask import Blueprint, jsonify
from models.emotion_model import detect_emotion
from routes.notifications import send_notification  # Push notification function

print(" Loading Instagram Blueprint...")

instagram_blueprint = Blueprint('instagram', __name__)

ACCESS_TOKEN = "IGAAiV0bk6tn5BZAE94aFFXM3lhcDI1OW0zRE1aTE4tOXBrS3RDaXVlTGRpZAGhfOEpOZAU9nWTZAkRG1MZA2F3MDVGM3RWWnBNSDVqdmpodldvby15d2tfZAFhXaEFvV1UybHNoQVpMdWtMZA0VYMkNEd1F2dC1IY2xGWER2RW5kQTQ5bwZDZD"
INSTAGRAM_BUSINESS_ID = "2416527802021502"

def fetch_instagram_posts():
    """Fetch latest Instagram posts & analyze emotions."""
    print(" Fetching Instagram Posts... (Currently Disabled)")

    #  Instagram API Integration is Pending
    return jsonify({"message": "Instagram fetching is temporarily disabled for this submission."})

    """
    url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_BUSINESS_ID}/media?fields=id,caption,timestamp&access_token={ACCESS_TOKEN}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            posts = response.json().get("data", [])
            print(f" Retrieved {len(posts)} posts from Instagram.")

            analyzed_posts = []
            for post in posts:
                caption = post.get("caption", "")
                if caption:
                    emotion = detect_emotion(caption)  # Your ML model
                    user_id = "test_user_123"  # Replace with actual user ID
                    message = f"Your Instagram post shows you are feeling {emotion}. Take care! ❤️"
                    send_notification(user_id, message)

                    analyzed_posts.append({
                        "id": post["id"],
                        "caption": caption,
                        "emotion": emotion
                    })

            print(f" {len(analyzed_posts)} posts analyzed and notifications sent.")
            return jsonify(analyzed_posts)

        else:
            print(f" Failed to fetch Instagram posts. Status Code: {response.status_code}")
            return jsonify({"error": "Failed to fetch Instagram posts"}), response.status_code

    except requests.RequestException as e:
        print(f" Error in fetch_instagram_posts: {e}")
        return jsonify({"error": "Instagram API request failed"}), 500
    """

#  **Expose API Route for Manual Testing**
@instagram_blueprint.route('/analyze-instagram-emotion', methods=['GET'])
def analyze_instagram_emotion():
    """Manually fetch & analyze Instagram posts"""
    return fetch_instagram_posts()
