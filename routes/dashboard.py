from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import User, Activity

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard", methods=["GET"])
@jwt_required()
def get_dashboard():

    # Current Logged-in User
    current_user = get_jwt_identity()

    # Allow only Admin
    if current_user["role"] != "Admin":
        return jsonify({
            "message": "Admin Access Required"
        }), 403

    # Dashboard Statistics
    total_users = User.query.count()
    total_activities = Activity.query.count()

    high_risk = Activity.query.filter(
        Activity.risk_score >= 80
    ).count()

    medium_risk = Activity.query.filter(
        (Activity.risk_score >= 50) &
        (Activity.risk_score < 80)
    ).count()

    low_risk = Activity.query.filter(
        Activity.risk_score < 50
    ).count()

    # Recent Activities
    recent = Activity.query.order_by(
        Activity.timestamp.desc()
    ).limit(5).all()

    recent_data = []

    for item in recent:
        recent_data.append({
            "id": item.id,
            "username": item.username,
            "action": item.action,
            "risk_score": item.risk_score,
            "timestamp": str(item.timestamp)
        })

    return jsonify({
        "total_users": total_users,
        "total_activities": total_activities,
        "high_risk_alerts": high_risk,
        "medium_risk_alerts": medium_risk,
        "low_risk_alerts": low_risk,
        "recent_activities": recent_data
    }), 200