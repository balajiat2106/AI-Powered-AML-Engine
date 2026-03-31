from config.settings import settings

def build_features(tx):
    return {
        "amount": tx.amount,
        "is_high_risk_country": 1 if tx.country in settings.high_risk_countries else 0,
        "hour_of_day": tx.timestamp.hour
    }