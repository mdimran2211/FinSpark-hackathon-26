from flask_jwt_extended import get_jwt_identity
from flask import jsonify

def check_admin():

    current_user = get_jwt_identity()

    if current_user["role"] != "Admin":
        return jsonify({
            "message": "Admin Access Required"
        }), 403

    return None