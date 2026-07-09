from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ---------------------------------
# User Model
# ---------------------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(50),
        nullable=False
    )


# ---------------------------------
# Activity Model
# ---------------------------------
class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        nullable=False
    )

    action = db.Column(
        db.String(200),
        nullable=False
    )

    # Network Information
    ip_address = db.Column(
        db.String(100),
        nullable=True
    )

    # Device Information
    device = db.Column(
        db.String(100),
        nullable=True
    )

    browser = db.Column(
        db.String(100),
        nullable=True
    )

    operating_system = db.Column(
        db.String(100),
        nullable=True
    )

    # Live Location
    location = db.Column(
        db.String(255),
        nullable=True
    )

    latitude = db.Column(
        db.Float,
        nullable=True
    )

    longitude = db.Column(
        db.Float,
        nullable=True
    )

    # AI Features
    login_hour = db.Column(
        db.Integer,
        nullable=False,
        default=9
    )

    failed_logins = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    files_accessed = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    usb_used = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    privilege_escalation = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    risk_score = db.Column(
        db.Float,
        default=0
    )

    timestamp = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )


# ---------------------------------
# Audit Log Model
# ---------------------------------
class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        nullable=False
    )

    event = db.Column(
        db.String(255),
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )