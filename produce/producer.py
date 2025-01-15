from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import NoBrokersAvailable
from kafka import KafkaProducer
import json
import pandas as pd
import time

KAFKA_TOPIC = "movielens"
KAFKA_BOOTSTRAP_SERVER = "kafka:9092"
MAX_CONNECTION_ATTEMPTS = 20


for i in range(MAX_CONNECTION_ATTEMPTS):
    try:
        print("Connecting to Kafka...")
        admin_client = KafkaAdminClient(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
            client_id="test",
        )
        print("Connected to Kafka")
        break
    except NoBrokersAvailable:
        print("No brokers available. Retrying...")
        time.sleep(5)
        continue


if "movielens" not in admin_client.list_topics():
    topic = NewTopic(name="movielens", num_partitions=1, replication_factor=1)
    admin_client.create_topics(new_topics=[topic], validate_only=False)


print("Loading data...")
ratings = pd.read_json("continual_train.json")
ratings = ratings.to_dict(orient="records")
print("Data loaded successfully")


kafka_producer_object = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)


# produce messages to Kafka
ctr = 0
for rating in ratings:
    print(f"{ctr} | Message sent")

    kafka_producer_object.send(KAFKA_TOPIC, rating)
    ctr += 1

    time.sleep(3)

    if ctr % 1000 == 0:
        print(f"Sent {ctr} messages")
        time.sleep(200)
