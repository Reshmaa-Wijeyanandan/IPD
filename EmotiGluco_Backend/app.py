from flask import Flask
from flask_cors import CORS
import threading
import time
from routes.instagram import fetch_instagram_posts  # Import function for background processing

# Import API Routes
from database import db  
from auth.auth import auth_blueprint
from routes.emotions import emotions_blueprint
from routes.glucose import glucose_blueprint
from routes.instagram import instagram_blueprint  
from routes.notifications import notifications_blueprint 

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Register API Routes
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(emotions_blueprint, url_prefix="/emotions")
app.register_blueprint(glucose_blueprint, url_prefix="/glucose")
app.register_blueprint(instagram_blueprint, url_prefix="/instagram")  
app.register_blueprint(notifications_blueprint, url_prefix="/notifications")  

#  **Temporarily Disabling Instagram Auto-Fetch**
"""
def background_instagram_fetch():
    '''Continuously fetch & analyze Instagram posts every 60 seconds'''
    while True:
        print(" Running background Instagram post fetch... (Currently Disabled)")
        try:
            fetch_instagram_posts()
        except Exception as e:
            print(f" Background Instagram fetch error: {e}")
        time.sleep(60)  # Fetch posts every 60 seconds

if __name__ == '__main__':
    print(" Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")

    #  Temporarily Disabling Background Instagram Fetching
    thread = threading.Thread(target=background_instagram_fetch, daemon=True)
    thread.start()
"""

if __name__ == '__main__':
    print(" Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")

    app.run(debug=True)
