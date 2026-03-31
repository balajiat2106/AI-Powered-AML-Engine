import pandas as pd
import numpy as np
import xgboost as xgb
import os

def train_dummy_model():
    print("Generating 10k rows of synthetic transaction data...")
    np.random.seed(42)
    
    amounts = np.random.exponential(scale=6000, size=10000)
    high_risk = np.random.choice([0, 1], size=10000, p=[0.9, 0.1])
    hours = np.random.randint(0, 24, size=10000)
    
    # Calculate a synthetic target label simulating fraud markers
    # e.g., huge amounts + high risk countries = usually flagged
    risk_scores = (amounts / 20000) + (high_risk * 0.6)
    labels = (risk_scores > 0.65).astype(int)

    # Scramble the labels slightly for realistic noise & imperfect accuracy
    noise = np.random.choice([0, 1], size=10000, p=[0.95, 0.05])
    labels = np.logical_xor(labels, noise).astype(int)

    df = pd.DataFrame({
        "amount": amounts,
        "is_high_risk_country": high_risk,
        "hour_of_day": hours
    })

    print("Training XGBoost Classifier...")
    model = xgb.XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.1)
    model.fit(df, labels)
    
    save_path = "src/risk_engine/inference/xgboost_model.json"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    model.save_model(save_path)
    print(f"Model saved successfully to {save_path}!")

if __name__ == "__main__":
    train_dummy_model()
