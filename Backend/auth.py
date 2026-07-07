from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from model import User
from db import db

auth_bp = Blueprint("auth", __name__) # Create a blueprint for auth routes





# JSON -----http --->request.get_json()----> Python dict---> process data ( check email and password) --> create response jsonify() --> JSON response to client
# ================= REGISTER =================
@auth_bp.route("/api/register", methods=["POST"])
def register():

    data = request.get_json() # request.get_json() is used to parse the incoming JSON data from the request body.
    # Returns a Python dictionary (or None if the request body isn’t valid JSON).


    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    role = data.get("role")

    if role not in ["student", "company"]:
        role = "student"  # Default to student if role is invalid or not provided

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400
 
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400

    new_user = User(
        name =name,
        email=email,
        password=generate_password_hash(password),
        role = role 
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201
# Converts Python objects (opps class etc.) into a JSON response with the 
# appropriate content type and status code. In this case, it returns a JSON object with a message 
# and a 201 status code indicating that the user was created successfully.







# ================= LOGIN =================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    
    print(f"Login attempt: {email}")
    

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        print("Login failed: Invalid email or password")
        return jsonify({"message": "Invalid email or password"}), 401

    access_token = create_access_token(identity=user.id)

    return jsonify({
        "token": access_token,
        "email": user.email,
        "role": user.role,
        "id": user.id
    }), 200




# with restfulAPIs we have a  ""marshaling""" process
#  that converts Python objects to JSON and vice versa. 
#  In this code, we are using jsonify() to convert Python dictionaries into JSON responses 