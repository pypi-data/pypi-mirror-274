import random

from io_.mobio.kafka_sdk.helpers.kafka_consumer_manager import BaseKafkaConsumer
from io_.mobio.kafka_sdk.helpers.kafka_producer_manager import KafkaProducerManager


class TestConsumer(BaseKafkaConsumer):

    def message_handle(self, data):
        print("data: {}".format(data))
        lst = [
            "127.0.0.1:9092",
            "kafka1:9092,kafka2:9092,kafka3:9092"
        ]
        KafkaProducerManager(random.choice(lst)).flush_message(topic="test1", key="a", value=data)


if __name__ == "__main__":
    TestConsumer(topic_name="test", group_id="test", client_mongo=None, retryable=False, bootstrap_server="127.0.0.1:9092")
