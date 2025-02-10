from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import db  # Import MongoDB connection
from bson import ObjectId

auth_blueprint = Blueprint('auth', __name__)

#  User Registration Route
@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    # Check if user exists in MongoDB
    if db.users.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 409

    # Hash password before storing
    hashed_pw = generate_password_hash(password)

    # Store user details in MongoDB
    new_user = db.users.insert_one({
        "full_name": full_name,
        "email": email,
        "password": hashed_pw
    })

    return jsonify({
        "message": "Registration successful",
        "user_id": str(new_user.inserted_id)  #  Return user_id for session storage
    }), 201

#  User Login Route
@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = db.users.find_one({"email": email})

    if user and check_password_hash(user["password"], password):
        return jsonify({
            "message": "Login successful",
            "user_id": str(user["_id"]),  #  Return user_id for session
            "full_name": user["full_name"],
            "email": user["email"]
        }), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

#  Get User Details Route (For Profile)
@auth_blueprint.route('/get-user', methods=['GET'])
def get_user():
    """Fetch user details by user_id"""
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    user = db.users.find_one({"_id": ObjectId(user_id)}, {"_id": 0})  #  Convert ObjectId & exclude MongoDB _id

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user), 200
