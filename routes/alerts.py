from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from database.models import Activity

alerts = Blueprint("alerts", __name__)


@alerts.route("/alerts", methods=["GET"])
@jwt_required()
def get_alerts():

    activities = (
        Activity.query
        .order_by(Activity.timestamp.desc())
        .all()
    )

    result = []

    for item in activities:

        event = None

        if item.risk_score >= 80:
            event = "High Risk Threat Detected"

        elif item.privilege_escalation:
            event = "Privilege Escalation Detected"

        elif item.usb_used:
            event = "USB Device Connected"

        elif item.failed_logins >= 5:
            event = f"Multiple Failed Logins ({item.failed_logins})"

        if event:

            result.append({

                "id": item.id,
                "username": item.username,
                "event": event,
                "risk_score": item.risk_score,
                "action": item.action,
                "ip_address": item.ip_address,
                "device": item.device,
                "location": item.location,
                "timestamp": str(item.timestamp)

            })

    return jsonify(result), 200