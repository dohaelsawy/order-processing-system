import logging
from app import app, users
from flask import request, jsonify
import bcrypt
from flask_jwt_extended import create_access_token


logger = logging.getLogger(__name__)


@app.post("/register")
def register_user():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")
        
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        if users.find_one({"email": email}):
            return jsonify({"error": "User already exists"}), 409
        
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        users.insert_one({
            "email": email,
            "password": hashed_password
        })
        
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        logger.error(f"Error occurred during user registration: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.post("/login")
def login_user():
    try:
        data = request.json
        email = data.get("email")
        user_password = data.get("password")
        
        if not email or not user_password:
            return jsonify({"error": "Email and password are required"}), 400
        
        user = users.find_one({"email": email})
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401
        
        hashed_password = user['password']
        if not bcrypt.checkpw(user_password.encode('utf-8'), hashed_password):
            return jsonify({"error": "Invalid credentials"}), 401
        
        token = create_access_token(identity=email)
        
        return jsonify({"message": "Login successful", "token": token}), 200
    except Exception as e:
        logger.error(f"Error occurred during user login: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
