def calculate_risk(marks):
    if marks >= 85:
        return "Low"
    elif marks >= 60:
        return "Medium"
    else:
        return "High"