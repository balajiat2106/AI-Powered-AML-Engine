import logging
import json
from datetime import datetime, timezone

# Setup JSON structured logger exclusively for auditing
json_logger = logging.getLogger("aml_audit")
json_logger.setLevel(logging.INFO)

# In production this would write to Kafka or ElasticSearch Logstash directly
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(message)s'))
json_logger.addHandler(handler)
# Prevent double streaming via root logger
json_logger.propagate = False  

def log_event(data: dict):
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "audit_event": data
    }
    json_logger.info(json.dumps(record))