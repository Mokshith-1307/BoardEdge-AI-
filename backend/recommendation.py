def generate_plan(subject, marks):

    if marks >= 85:
        confidence = "High"
        course = f"{subject} Advanced Excellence Program"
    elif marks >= 60:
        confidence = "Medium"
        course = f"{subject} Booster Program"
    else:
        confidence = "Low"
        course = f"{subject} Foundation Recovery Program"

    weekly_plan = [
        "Week 1: Core Concept Revision",
        "Week 2: Chapter-wise Practice",
        "Week 3: Mock Tests & Analysis",
        "Week 4: Final Revision & Weak Area Focus"
    ]

    return {
        "confidence": confidence,
        "course": course,
        "weekly_plan": weekly_plan
    }