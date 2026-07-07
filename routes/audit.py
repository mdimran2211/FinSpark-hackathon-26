from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import AuditLog, User

audit = Blueprint("audit", __name__)


@audit.route("/audit", methods=["GET"])
@jwt_required()
def get_audit_logs():

    username = get_jwt_identity()

    user = User.query.filter_by(username=username).first()

    if user is None:
        return jsonify({
            "message": "User not found"
        }), 404

    if user.role != "Admin":
        return jsonify({
            "message": "Admin Access Required"
        }), 403

    logs = AuditLog.query.order_by(
        AuditLog.timestamp.desc()
    ).all()

    result = []

    for log in logs:
        result.append({
            "id": log.id,
            "username": log.username,
            "event": log.event,
            "timestamp": str(log.timestamp)
        })

    return jsonify(result), 200