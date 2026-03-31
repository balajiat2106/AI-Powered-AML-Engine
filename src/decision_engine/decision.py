from config.settings import settings

def make_decision(risk_score: float):
    if risk_score > settings.escalate_threshold:
        return "ESCALATE"
    elif risk_score > settings.review_threshold:
        return "REVIEW"
    return "ALLOW"