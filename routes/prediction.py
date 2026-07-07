from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ml.predict import predict_threat
from utils.risk_score import calculate_risk
from utils.alerts import generate_alert

prediction = Blueprint("prediction", __name__)


@prediction.route("/predict", methods=["POST"])
@jwt_required()
def predict():

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

    # AI Prediction
    prediction = predict_threat(
        login_hour,
        failed_logins,
        files_accessed,
        usb_used,
        privilege_escalation
    )

    # Rule-based Risk Score
    risk_score = calculate_risk(action)

    # Increase score if AI detects anomaly
    if prediction in ["Suspicious", "Anomaly", "High Risk"]:
        risk_score = min(risk_score + 20, 100)

    # Final Prediction based on Risk Score
    if risk_score >= 80:
        final_prediction = "High Risk"
    elif risk_score >= 50:
        final_prediction = "Medium Risk"
    else:
        final_prediction = "Low Risk"

    alert = generate_alert(risk_score)

    return jsonify({
        "ai_prediction": prediction,
        "final_prediction": final_prediction,
        "risk_score": risk_score,
        "alert": alert
    }), 200