def explain(features, risk_score):
    return {
        "top_features": sorted(features.items(), key=lambda x: -x[1])[:2],
        "reason": "High amount and/or high-risk geography contributed to risk score"
    }