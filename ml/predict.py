import joblib
import os

# Load trained model
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
model = joblib.load(model_path)


def predict_threat(
    login_hour,
    failed_logins,
    files_accessed,
    usb_used,
    privilege_escalation
):
    data = [[
        login_hour,
        failed_logins,
        files_accessed,
        usb_used,
        privilege_escalation
    ]]

    prediction = model.predict(data)

    if prediction[0] == -1:
        return "Suspicious"
    else:
        return "Normal"