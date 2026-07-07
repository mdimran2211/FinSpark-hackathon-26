import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

# -----------------------------
# Load Dataset
# -----------------------------
dataset_path = os.path.join(os.path.dirname(__file__), "dataset.csv")

data = pd.read_csv(dataset_path)

# -----------------------------
# Select Features
# -----------------------------
X = data[[
    "login_hour",
    "failed_logins",
    "files_accessed",
    "usb_used",
    "privilege_escalation"
]]

# -----------------------------
# Train Isolation Forest Model
# -----------------------------
model = IsolationForest(
    n_estimators=100,
    contamination=0.2,
    random_state=42
)

model.fit(X)

# -----------------------------
# Save Model
# -----------------------------
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")

joblib.dump(model, model_path)

print("===================================")
print(" AI Model Trained Successfully!")
print(" Model saved as ml/model.pkl")
print("===================================")