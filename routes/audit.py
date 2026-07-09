from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.models import AuditLog, User, Activity

audit = Blueprint("audit", __name__)


# ---------------------------------
# Audit Logs API
# ---------------------------------
@audit.route("/audit", methods=["GET"])
@jwt_required()
def get_audit_logs():

    username = get_jwt_identity()

    user = User.query.filter_by(
        username=username
    ).first()

    if user is None:
        return jsonify({
            "message": "User Not Found"
        }), 404

    logs = (
        AuditLog.query
        .order_by(AuditLog.timestamp.desc())
        .all()
    )

    result = []

    for log in logs:

        result.append({

            "id": log.id,
            "username": log.username,
            "event": log.event,
            "timestamp": str(log.timestamp)

        })

    return jsonify(result), 200


# ---------------------------------
# Live Alerts API
# ---------------------------------
@audit.route("/alerts", methods=["GET"])
@jwt_required()
def get_alerts():

    activities = (
        Activity.query
        .order_by(Activity.timestamp.desc())
        .limit(10)
        .all()
    )

    alerts = []

    for item in activities:

        if item.risk_score >= 80:
            level = "Critical"

        elif item.risk_score >= 60:
            level = "High"

        elif item.risk_score >= 40:
            level = "Medium"

        else:
            level = "Low"

        alerts.append({

            "id": item.id,

            "username": item.username,

            "action": item.action,

            "risk_score": item.risk_score,

            "alert_level": level,

            "ip_address": item.ip_address,

            "device": item.device,

            "timestamp": str(item.timestamp)

        })

    return jsonify({

        "total_alerts": len(alerts),

        "alerts": alerts

    }), 200