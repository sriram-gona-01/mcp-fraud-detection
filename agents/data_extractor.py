import os, json
from kafka import KafkaConsumer
from langgraph import Agent

class DataExtractor(Agent):
    def run(self):
        consumer = KafkaConsumer(
            os.getenv("KAFKA_TOPIC"),
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP")
        )
        for msg in consumer:
            record = json.loads(msg.value)
            self.emit("raw_txn", record)
