from database.models import db, AuditLog


def save_audit(username, event):
    log = AuditLog(
        username=username,
        event=event
    )

    db.session.add(log)
    db.session.commit()