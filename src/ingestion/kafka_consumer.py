import json
import logging
from confluent_kafka import Consumer, KafkaError, KafkaException
from pydantic import ValidationError
from config.settings import settings
from src.schemas.transaction import Transaction
from src.orchestration.pipeline import run_pipeline
from src.database.connection import engine, Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aml_consumer")

# Ensure tables exist on consumer boot as well in case API boots slower
Base.metadata.create_all(bind=engine)

def process_message(msg_value):
    try:
        data = json.loads(msg_value)
        tx = Transaction(**data)
        logger.info(f"Processing transaction '{tx.transaction_id}' via Kafka stream...")
        run_pipeline(tx)
    except ValidationError as e:
        logger.error(f"Validation error for incoming Kafka message: {e}")
    except json.JSONDecodeError:
        logger.error("Failed to decode Kafka message as JSON")
    except Exception as e:
        logger.error(f"Pipeline error during Kafka consumption: {e}")

def run_consumer():
    conf = {
        'bootstrap.servers': settings.kafka_broker,
        'group.id': 'aml_pipeline_group',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(conf)
    
    try:
        consumer.subscribe([settings.kafka_topic])
        logger.info(f"Subscribed to topic '{settings.kafka_topic}' on {settings.kafka_broker}")

        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    raise KafkaException(msg.error())
                    
            process_message(msg.value().decode('utf-8'))
            
    except KeyboardInterrupt:
        logger.info("Consumer interrupted by user.")
    finally:
        consumer.close()
        logger.info("Kafka consumer closed.")

if __name__ == "__main__":
    run_consumer()
