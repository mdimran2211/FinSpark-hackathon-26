from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from database.models import db, User
from utils.audit import save_audit
import bcrypt

auth = Blueprint("auth", __name__)


# ---------------------------------
# Register API
# ---------------------------------
@auth.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    if not username or not password or not role:
        return jsonify({
            "message": "Username, Password and Role are required"
        }), 400

    # User Exists?
    existing_user = User.query.filter_by(
        username=username
    ).first()

    if existing_user:

        save_audit(username, "Registration Failed (Username Already Exists)")

        return jsonify({
            "message": "Username already exists"
        }), 400

    # Hash Password
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    # Save User
    new_user = User(
        username=username,
        password=hashed_password,
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    # Audit Log
    save_audit(
        username,
        f"New User Registered ({role})"
    )

    return jsonify({
        "message": "User Registered Successfully"
    }), 201


# ---------------------------------
# Login API
# ---------------------------------
@auth.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "message": "Username and Password are required"
        }), 400

    # Find User
    user = User.query.filter_by(
        username=username
    ).first()

    if user is None:

        save_audit(
            username,
            "Login Failed (Invalid Username)"
        )

        return jsonify({
            "message": "Invalid Username"
        }), 401

    # Verify Password
    if not bcrypt.checkpw(
        password.encode("utf-8"),
        user.password.encode("utf-8")
    ):

        save_audit(
            username,
            "Login Failed (Wrong Password)"
        )

        return jsonify({
            "message": "Invalid Password"
        }), 401

    # Successful Login
    access_token = create_access_token(
        identity=user.username
    )

    # Audit Log
    save_audit(
        username,
        "User Logged In Successfully"
    )

    return jsonify({
        "message": "Login Successful",
        "access_token": access_token,
        "username": user.username,
        "role": user.role
    }), 200