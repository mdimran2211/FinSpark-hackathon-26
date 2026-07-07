from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import db, Activity
from utils.risk_score import calculate_risk
from utils.alerts import generate_alert

activity = Blueprint("activity", __name__)


# -----------------------------
# Save Activity API
# -----------------------------
@activity.route("/activity", methods=["POST"])
@jwt_required()
def save_activity():

    data = request.get_json()

    # Logged-in user from JWT
    username = get_jwt_identity()

    action = data.get("action")
    ip_address = data.get("ip_address")
    device = data.get("device")

    if not action or not ip_address or not device:
        return jsonify({
            "message": "Action, IP Address and Device are required"
        }), 400

    # Calculate Risk Score
    risk_score = calculate_risk(action)

    # Generate Alert
    alert = generate_alert(risk_score)

    # Save Activity
    new_activity = Activity(
        username=username,
        action=action,
        ip_address=ip_address,
        device=device,
        risk_score=risk_score
    )

    db.session.add(new_activity)
    db.session.commit()

    return jsonify({
        "message": "Activity Saved Successfully",
        "username": username,
        "risk_score": risk_score,
        "alert": alert
    }), 201


# -----------------------------
# Get All Activities API
# -----------------------------
@activity.route("/activities", methods=["GET"])
@jwt_required()
def get_activities():

    activities = Activity.query.order_by(Activity.timestamp.desc()).all()

    result = []

    for item in activities:
        result.append({
            "id": item.id,
            "username": item.username,
            "action": item.action,
            "ip_address": item.ip_address,
            "device": item.device,
            "risk_score": item.risk_score,
            "timestamp": str(item.timestamp)
        })

    return jsonify(result), 200