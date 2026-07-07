def calculate_risk(action):

    high_risk = [
        "Sensitive File Access",
        "Delete File",
        "Admin Login",
        "USB Connected",
        "Privilege Escalation"
    ]

    medium_risk = [
        "Download File",
        "Upload File",
        "Password Change"
    ]

    if action in high_risk:
        return 90

    elif action in medium_risk:
        return 60

    return 20