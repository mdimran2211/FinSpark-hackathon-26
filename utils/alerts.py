def generate_alert(score):

    if score >= 80:
        return "HIGH"

    elif score >= 50:
        return "MEDIUM"

    return "LOW"