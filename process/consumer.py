from kafka import KafkaConsumer
import json
import NLP

KAFKA_TOPIC = "movielens"
KAFKA_BOOTSTRAP_SERVER = "kafka:9092"
MAX_BUFFER_SIZE = 10

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
    auto_offset_reset="earliest",  # Start reading at the earliest message
    enable_auto_commit=True,  # Commit offsets automatically
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

model = NLP.load_model("Model.keras")
model.save("/shared_volume/Model.keras")

vectoriser = NLP.Load_Vectorizer("Model.ftz")

buffer = []

print("Connected to Kafka and listening for messages...")
try:
    ctr = 0

    # process stream of data
    for message in consumer:
        if ctr % 100 == 0:
            print(f"Message {ctr}")

        ctr += 1

        data = message.value

        msg = data.get("0")
        categories = data.get("1")
        buffer.append([msg, categories])

        if len(buffer) > MAX_BUFFER_SIZE:
            print("Buffer full. Preparing buffer for retraining...")

            iterator = 0
            X = []
            Y = []

            for d in buffer:
                processed_point = NLP.Process_Point(d, vectoriser)

                X.append(processed_point[0])
                Y.append(processed_point[1])

                iterator += 1

                if iterator % 100 == 0:
                    print(str(round(iterator * 10000 / len(data)) / 100.0) + "%")

            print("Retraining model...")

            NLP.Train_Model(
                X,
                Y,
                1000,
                Learning_Rate=0.00001,
                Name="/shared_volume/Model",
                Previous_Model=NLP.load_model("/shared_volume/Model.keras"),
            )

            buffer = []
            print("Model retrained. Buffer cleared.")


except KeyboardInterrupt:
    print("Consumer stopped.")


finally:
    # Close the consumer connection
    consumer.close()
    print("Kafka consumer closed.")
