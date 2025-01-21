import os
from dotenv import load_dotenv
from kafka import KafkaProducer

class DCKafkaClient():
    """
    Handles all Kafka interactions in the Data Collection component.
    """
    @classmethod
    def __init__(self):
        load_dotenv()
        self._kafkaBroker = os.getenv("KAFKA_BROKER_ADDRESS")

    @classmethod
    def sendToRedditTopic(self, message: str):
        """
        Sends a message to the "reddit" Kafka topic.
        """
        producer = KafkaProducer(bootstrap_servers=self._kafkaBroker)
        producer.send("reddit", message.encode())
        producer.flush()
        producer.close()