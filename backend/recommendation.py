from risk_engine import calculate_risk

def generate_plan(data):
    grade = data.get("grade")
    subject = data.get("weak_subject")
    score = int(data.get("score"))
    learning_style = data.get("learning_style")

    # Risk assessment
    risk = calculate_risk(score)

    # Confidence scoring logic
    confidence = 0
    if subject:
        confidence += 40
    if learning_style == "Video":
        confidence += 30
    if grade:
        confidence += 20
    if score < 75:
        confidence += 10

    # Weekly structured plan
    weekly_plan = [
        "Week 1: Core Concept Revision",
        "Week 2: Chapter-wise Practice",
        "Week 3: Timed Mock Tests",
        "Week 4: Weak Area Reinforcement"
    ]

    explanation = [
        f"Detected academic score: {score}",
        f"Risk level assessed as: {risk}",
        f"Learning preference identified as: {learning_style}",
        "Generated structured 4-week board preparation plan"
    ]

    return {
        "risk_level": risk,
        "confidence_score": confidence,
        "recommended_course": f"{subject} Board Mastery Program",
        "weekly_plan": weekly_plan,
        "why_this_plan": explanation
    }
