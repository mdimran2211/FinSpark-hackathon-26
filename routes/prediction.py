from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ml.predict import predict_threat
from utils.risk_score import calculate_risk
from utils.alerts import generate_alert
from utils.audit import save_audit

prediction = Blueprint("prediction", __name__)


# ---------------------------------
# AI Prediction API
# ---------------------------------
@prediction.route("/predict", methods=["POST"])
@jwt_required()
def predict():

    username = get_jwt_identity()

    data = request.get_json()

    login_hour = data.get("login_hour")
    failed_logins = data.get("failed_logins")
    files_accessed = data.get("files_accessed")
    usb_used = data.get("usb_used")
    privilege_escalation = data.get("privilege_escalation")
    action = data.get("action", "Normal Login")

    if None in (
        login_hour,
        failed_logins,
        files_accessed,
        usb_used,
        privilege_escalation,
    ):
        return jsonify({
            "message": "All fields are required"
        }), 400

    # -----------------------------
    # AI Prediction
    # -----------------------------
    ai_prediction = predict_threat(
        login_hour,
        failed_logins,
        files_accessed,
        usb_used,
        privilege_escalation
    )

    # -----------------------------
    # Rule-Based Risk Score
    # -----------------------------
    risk_score = calculate_risk(action)

    if ai_prediction in [
        "Suspicious",
        "Anomaly",
        "High Risk"
    ]:
        risk_score = min(risk_score + 20, 100)

    # -----------------------------
    # Final Prediction
    # -----------------------------
    if risk_score >= 80:
        final_prediction = "High Risk"

    elif risk_score >= 50:
        final_prediction = "Medium Risk"

    else:
        final_prediction = "Low Risk"

    # -----------------------------
    # Alert
    # -----------------------------
    alert = generate_alert(risk_score)

    # -----------------------------
    # Save Audit Logs
    # -----------------------------
    save_audit(
        username,
        f"AI Prediction: {final_prediction} | Risk Score: {risk_score}%"
    )

    if usb_used == 1:
        save_audit(
            username,
            "USB Device Connected"
        )

    if privilege_escalation == 1:
        save_audit(
            username,
            "Privilege Escalation Detected"
        )

    if failed_logins >= 5:
        save_audit(
            username,
            f"Multiple Failed Logins ({failed_logins})"
        )

    # -----------------------------
    # Response
    # -----------------------------
    return jsonify({
        "username": username,
        "ai_prediction": ai_prediction,
        "final_prediction": final_prediction,
        "risk_score": risk_score,
        "alert": alert
    }), 200