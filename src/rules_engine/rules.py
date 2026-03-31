from config.settings import settings

def apply_rules(tx, features):
    flags = []

    if tx.amount > settings.high_value_tx_threshold:
        flags.append("HIGH_VALUE_TX")

    if features.get("is_high_risk_country") == 1:
        flags.append("HIGH_RISK_COUNTRY")

    return flags