import os
import xgboost as xgb
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class RiskModel:
    def __init__(self):
        self.model = xgb.XGBClassifier()
        model_path = os.path.join(os.path.dirname(__file__), "xgboost_model.json")
        try:
            self.model.load_model(model_path)
            # Just to guarantee it's initialized appropriately
            logger.info("Successfully loaded XGBoost risk model.")
        except Exception as e:
            logger.warning(f"Could not load XGBoost model from {model_path}. Using fallback logic. Error: {e}")
            self.model = None

    def predict(self, features: dict) -> float:
        if self.model is None:
            # Fallback heuristic logic if training script wasn't run
            base = features.get("amount", 0) / 10000.0
            risk = min(1.0, base + features.get("is_high_risk_country", 0) * 0.5)
            return round(risk, 3)

        # XGBoost expects a Pandas DataFrame matching exact training feature names
        df = pd.DataFrame([features])
        
        # predict_proba returns [[prob_class_0, prob_class_1]]
        probability_of_fraud = self.model.predict_proba(df)[0][1]
        
        return round(float(probability_of_fraud), 3)