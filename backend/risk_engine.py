def calculate_risk(score):
    if score < 40:
        return "High"
    elif score < 75:
        return "Moderate"
    else:
        return "Low"
