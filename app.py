from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

import config

from database.models import db

# -----------------------------
# Import Blueprints
# -----------------------------
from routes.auth import auth
from routes.activity import activity
from routes.prediction import prediction
from routes.dashboard import dashboard
from routes.audit import audit
from routes.alerts import alerts

# -----------------------------
# Create Flask App
# -----------------------------
app = Flask(__name__)

# -----------------------------
# Load Configuration
# -----------------------------
app.config.from_object(config)

# -----------------------------
# Enable CORS
# -----------------------------
CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
            ]
        }
    },
    supports_credentials=True,
)

# -----------------------------
# Initialize Extensions
# -----------------------------
db.init_app(app)
jwt = JWTManager(app)

# -----------------------------
# Create Database
# -----------------------------
with app.app_context():
    db.create_all()

# -----------------------------
# Register Blueprints
# -----------------------------
app.register_blueprint(auth)
app.register_blueprint(activity)
app.register_blueprint(prediction)
app.register_blueprint(dashboard)
app.register_blueprint(audit)
app.register_blueprint(alerts)

# -----------------------------
# Home
# -----------------------------
@app.route("/")
def home():

    return jsonify({

        "status": "success",

        "message": "ThreatShield AI Backend Running",

        "project": "AI Powered Insider Threat Detection System",

        "version": "2.1",

        "developer": "Hackathon Team"

    })


# -----------------------------
# Health Check
# -----------------------------
@app.route("/health")
def health():

    return jsonify({

        "status": "healthy",

        "database": "connected",

        "server": "running"

    })


# -----------------------------
# API Information
# -----------------------------
@app.route("/api")
def api():

    return jsonify({

        "project": "ThreatShield AI",

        "version": "2.1",

        "apis": [

            {
                "method": "POST",
                "endpoint": "/register",
                "description": "Register User"
            },

            {
                "method": "POST",
                "endpoint": "/login",
                "description": "Login User"
            },

            {
                "method": "POST",
                "endpoint": "/activity",
                "description": "Save User Activity"
            },

            {
                "method": "GET",
                "endpoint": "/activities",
                "description": "All Activities"
            },

            {
                "method": "GET",
                "endpoint": "/current-activity",
                "description": "Current User Activity"
            },

            {
                "method": "POST",
                "endpoint": "/predict",
                "description": "AI Threat Prediction"
            },

            {
                "method": "GET",
                "endpoint": "/dashboard",
                "description": "Dashboard Statistics"
            },

            {
                "method": "GET",
                "endpoint": "/audit",
                "description": "Audit Logs"
            },

            {
                "method": "GET",
                "endpoint": "/alerts",
                "description": "Security Alerts"
            }

        ]

    })


# -----------------------------
# 404 Handler
# -----------------------------
@app.errorhandler(404)
def page_not_found(e):

    return jsonify({

        "status": "error",

        "message": "Endpoint Not Found"

    }), 404


# -----------------------------
# 500 Handler
# -----------------------------
@app.errorhandler(500)
def internal_error(e):

    return jsonify({

        "status": "error",

        "message": "Internal Server Error"

    }), 500


# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )