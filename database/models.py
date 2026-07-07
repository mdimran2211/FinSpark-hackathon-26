from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# -----------------------------
# User Model
# -----------------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)


# -----------------------------
# Activity Model
# -----------------------------
class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False)

    action = db.Column(db.String(200), nullable=False)

    ip_address = db.Column(db.String(100), nullable=False)

    device = db.Column(db.String(100), nullable=False)

    risk_score = db.Column(db.Float, default=0)

    timestamp = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )


# -----------------------------
# Audit Log Model
# -----------------------------
class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False)

    event = db.Column(db.String(255), nullable=False)

    timestamp = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )