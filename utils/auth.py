from flask_jwt_extended import get_jwt_identity
from flask import jsonify

from database.models import User


def check_admin():

    username = get_jwt_identity()

    user = User.query.filter_by(
        username=username
    ).first()

    if user is None:
        return jsonify({
            "message": "User Not Found"
        }), 404

    if user.role != "Admin":
        return jsonify({
            "message": "Admin Access Required"
        }), 403

    return None