from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    app_name: str = "AI-Powered AML Engine"
    
    # Engine Settings
    escalate_threshold: float = 0.85
    review_threshold: float = 0.60
    high_value_tx_threshold: float = 10000.0
    high_risk_countries: List[str] = ["IR", "KP", "SY", "CU"]
    
    # Infrastructure defaults (overridden by docker environment variables)
    database_url: str = "postgresql://postgres:password@localhost:5432/aml_db"
    kafka_broker: str = "localhost:9092"
    kafka_topic: str = "aml_transactions"

    class Config:
        env_file = ".env"

settings = Settings()
