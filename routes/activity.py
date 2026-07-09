from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.models import db, Activity
from utils.risk_score import calculate_risk
from utils.alerts import generate_alert

activity = Blueprint("activity", __name__)


# ---------------------------------
# Save Activity API
# ---------------------------------
@activity.route("/activity", methods=["POST"])
@jwt_required()
def save_activity():

    data = request.get_json()

    username = get_jwt_identity()

    # Basic Information
    action = data.get("action")
    ip_address = data.get("ip_address", "Unknown")

    # Device Information
    device = data.get("device", "Unknown")
    browser = data.get("browser", "Unknown")
    operating_system = data.get("operating_system", "Unknown")

    # Live Location
    location = data.get("location", "Unknown")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if not action:
        return jsonify({
            "message": "Action is required"
        }), 400

    # AI Features
    login_hour = data.get("login_hour", 9)
    failed_logins = data.get("failed_logins", 0)
    files_accessed = data.get("files_accessed", 0)
    usb_used = data.get("usb_used", False)
    privilege_escalation = data.get("privilege_escalation", False)

    # Calculate Risk
    risk_score = calculate_risk(action)

    # Alert
    alert = generate_alert(risk_score)

    # Save Activity
    new_activity = Activity(

        username=username,

        action=action,

        ip_address=ip_address,

        device=device,

        browser=browser,

        operating_system=operating_system,

        location=location,

        latitude=latitude,

        longitude=longitude,

        login_hour=login_hour,

        failed_logins=failed_logins,

        files_accessed=files_accessed,

        usb_used=usb_used,

        privilege_escalation=privilege_escalation,

        risk_score=risk_score

    )

    db.session.add(new_activity)
    db.session.commit()

    return jsonify({

        "message": "Activity Saved Successfully",

        "username": username,

        "location": location,

        "device": device,

        "browser": browser,

        "operating_system": operating_system,

        "risk_score": risk_score,

        "alert": alert

    }), 201


# ---------------------------------
# Get All Activities
# ---------------------------------
@activity.route("/activities", methods=["GET"])
@jwt_required()
def get_activities():

    activities = Activity.query.order_by(
        Activity.timestamp.desc()
    ).all()

    result = []

    for item in activities:

        result.append({

            "id": item.id,

            "username": item.username,

            "action": item.action,

            "ip_address": item.ip_address,

            "device": item.device,

            "browser": item.browser,

            "operating_system": item.operating_system,

            "location": item.location,

            "latitude": item.latitude,

            "longitude": item.longitude,

            "login_hour": item.login_hour,

            "failed_logins": item.failed_logins,

            "files_accessed": item.files_accessed,

            "usb_used": item.usb_used,

            "privilege_escalation": item.privilege_escalation,

            "risk_score": item.risk_score,

            "timestamp": str(item.timestamp)

        })

    return jsonify(result), 200


# ---------------------------------
# Current Activity
# ---------------------------------
@activity.route("/current-activity", methods=["GET"])
@jwt_required()
def current_activity():

    username = get_jwt_identity()

    latest = (
        Activity.query
        .filter_by(username=username)
        .order_by(Activity.timestamp.desc())
        .first()
    )

    if latest is None:

        return jsonify({

            "username": username,

            "login_hour": 9,

            "failed_logins": 0,

            "files_accessed": 0,

            "usb_used": False,

            "privilege_escalation": False,

            "action": "Normal Login",

            "ip_address": "Unknown",

            "device": "Desktop",

            "browser": "Unknown",

            "operating_system": "Unknown",

            "location": "Unknown",

            "latitude": None,

            "longitude": None

        }), 200

    return jsonify({

        "username": latest.username,

        "action": latest.action,

        "ip_address": latest.ip_address,

        "device": latest.device,

        "browser": latest.browser,

        "operating_system": latest.operating_system,

        "location": latest.location,

        "latitude": latest.latitude,

        "longitude": latest.longitude,

        "login_hour": latest.login_hour,

        "failed_logins": latest.failed_logins,

        "files_accessed": latest.files_accessed,

        "usb_used": latest.usb_used,

        "privilege_escalation": latest.privilege_escalation,

        "risk_score": latest.risk_score,

        "timestamp": str(latest.timestamp)

    }), 200