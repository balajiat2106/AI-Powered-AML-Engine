from sqlalchemy import Column, Integer, String, Float, DateTime
from src.database.connection import Base
from datetime import datetime, timezone

class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(Integer, primary_key=True, index=True)
    tx_id = Column(String, index=True)
    risk_score = Column(Float)
    decision = Column(String)
    narrative = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
