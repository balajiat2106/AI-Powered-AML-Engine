import logging
import json
from datetime import datetime, timezone
from src.database.connection import SessionLocal
from src.audit.models import AuditEvent

# Setup JSON structured logger exclusively for auditing
json_logger = logging.getLogger("aml_audit")
json_logger.setLevel(logging.INFO)

# In production this would write to ElasticSearch Logstash directly
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(message)s'))
json_logger.addHandler(handler)
# Prevent double streaming via root logger
json_logger.propagate = False  

def log_event(data: dict):
    # Log JSON for observability streams
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "audit_event": data
    }
    json_logger.info(json.dumps(record))
    
    # Persist structured event to PostgreSQL
    try:
        with SessionLocal() as db:
            db_event = AuditEvent(
                tx_id=data.get("tx_id"),
                risk_score=data.get("risk_score"),
                decision=data.get("decision"),
                narrative=data.get("narrative")
            )
            db.add(db_event)
            db.commit()
    except Exception as e:
        # Prevent database logging failures from crashing the orchestration layer
        logging.getLogger(__name__).error(f"Failed to persist audit to Postgres: {str(e)}")