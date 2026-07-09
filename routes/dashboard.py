from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.models import User, Activity

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard", methods=["GET"])
@jwt_required()
def get_dashboard():

    username = get_jwt_identity()

    current_user = User.query.filter_by(
        username=username
    ).first()

    if current_user is None:
        return jsonify({
            "message": "User Not Found"
        }), 404

    # Dashboard Statistics
    total_users = User.query.count()

    total_activities = Activity.query.count()

    high_risk = Activity.query.filter(
        Activity.risk_score >= 80
    ).count()

    medium_risk = Activity.query.filter(
        Activity.risk_score >= 40,
        Activity.risk_score < 80
    ).count()

    low_risk = Activity.query.filter(
        Activity.risk_score < 40
    ).count()

    recent = (
        Activity.query
        .order_by(Activity.timestamp.desc())
        .limit(5)
        .all()
    )

    recent_data = []

    for item in recent:

        recent_data.append({

            "id": item.id,
            "username": item.username,
            "action": item.action,
            "risk_score": item.risk_score,
            "ip_address": item.ip_address,
            "device": item.device,
            "timestamp": str(item.timestamp)

        })

    return jsonify({

        "username": current_user.username,
        "role": current_user.role,

        "total_users": total_users,
        "total_activities": total_activities,

        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,

        "recent_activities": recent_data

    }), 200