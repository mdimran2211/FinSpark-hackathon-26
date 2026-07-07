from flask import Flask
from flask_jwt_extended import JWTManager

import config

from database.models import db

# Import Routes
from routes.auth import auth
from routes.activity import activity
from routes.prediction import prediction
from routes.dashboard import dashboard
from routes.audit import audit


# ---------------------------------
# Create Flask App
# ---------------------------------
app = Flask(__name__)


# ---------------------------------
# Load Configuration
# ---------------------------------
app.config.from_object(config)


# ---------------------------------
# Initialize Extensions
# ---------------------------------
db.init_app(app)
jwt = JWTManager(app)


# ---------------------------------
# Create Database Tables
# ---------------------------------
with app.app_context():
    db.create_all()


# ---------------------------------
# Register Blueprints
# ---------------------------------
app.register_blueprint(auth)
app.register_blueprint(activity)
app.register_blueprint(prediction)
app.register_blueprint(dashboard)
app.register_blueprint(audit)


# ---------------------------------
# Home Route
# ---------------------------------
@app.route("/")
def home():
    return {
        "status": "success",
        "message": "Insider Threat Detection Backend Running",
        "version": "1.0",
        "developer": "Hackathon Team"
    }


# ---------------------------------
# Health Check Route
# ---------------------------------
@app.route("/health")
def health():
    return {
        "status": "healthy",
        "database": "connected",
        "server": "running"
    }


# ---------------------------------
# API Information
# ---------------------------------
@app.route("/api")
def api():

    return {
        "apis": [

            {
                "method": "POST",
                "endpoint": "/register"
            },

            {
                "method": "POST",
                "endpoint": "/login"
            },

            {
                "method": "POST",
                "endpoint": "/activity"
            },

            {
                "method": "GET",
                "endpoint": "/activities"
            },

            {
                "method": "POST",
                "endpoint": "/predict"
            },

            {
                "method": "GET",
                "endpoint": "/dashboard"
            },

            {
                "method": "GET",
                "endpoint": "/audit"
            }

        ]
    }


# ---------------------------------
# Run Server
# ---------------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )