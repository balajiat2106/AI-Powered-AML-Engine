import random

class RiskModel:
    def predict(self, features: dict) -> float:
        # TODO: Replace with real model (XGBoost / Torch)
        base = features["amount"] / 10000
        risk = min(1.0, base + features["is_high_risk_country"] * 0.5)
        return round(risk, 3)