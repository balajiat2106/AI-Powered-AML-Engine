from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class Transaction(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    transaction_id: str
    user_id: str
    amount: float = Field(..., ge=0, description="Amount must be positive")
    country: str = Field(..., min_length=2, max_length=2, description="2-letter ISO country code")
    timestamp: datetime
    merchant: Optional[str] = None