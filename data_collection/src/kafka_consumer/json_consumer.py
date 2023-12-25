import argparse

from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry.json_schema import JSONDeserializer
from src.entity.generic import Generic
from src.kafka_config import sasl_conf
from src.database.mongodb import MongodbOperation


def consumer_using_sample_file(topic, file_path):
    # Step 2: Get the schema to consume data=======================================================
    schema_str = Generic.get_schema_to_produce_consume_data(file_path=file_path)

    # Step 3: Define the deserializor==============================================
    json_deserializer = JSONDeserializer(schema_str, from_dict=Generic.dict_to_object)

    # Step 4: Get the Schema Registry config for consumer and specify a group name to identify the consumer group uniquely==========================
    consumer_conf = sasl_conf()
    # This is to identify the consumer group, and starting point of the consumer.
    consumer_conf.update({"group.id": "group1", "auto.offset.reset": "earliest"})

    # Create the Consumer object, and pass the Kafka cluster congifuration
    consumer = Consumer(consumer_conf)
    # Subscribe to topic and start consuming. Subsciption to multiple topics can be done here. Just add the topic name to the list.
    # Subscribtion allows the consumer to get the data from multiple topics.
    consumer.subscribe([topic])

    # Step 5: Start consuming the data==========================================================
    # Create the mongodb object to insert the data into mongodb
    mongodb = MongodbOperation()
    # records list to store the 5000 sensor records before sending to mongodb.
    # randomly chosen number, can be changed if optimal number is found to speed up the process.
    records = []
    x = 0
    while True:
        try:
            # SIGINT can't be handled when polling, limit timeout to 1 second.
            msg = consumer.poll(1.0)
            # If message is None, continue to the next message and skip rest of the code after this if statement.
            if msg is None:
                continue

            # Deserialize the message into dictionary using JSONDeserializer, then from dictionary to object using dict_to_object method.
            record: Generic = json_deserializer(
                msg.value(), SerializationContext(msg.topic(), MessageField.VALUE)
            )

            # mongodb.insert(collection_name="car",record=car.record)

            # Step 6: store 5000 sensor records, once 5000 limit reached, then insert into mongodb, then empty the records list======================
            if record is not None:
                records.append(record.to_dict())
                if x % 5000 == 0:
                    # Step 7: Insert many records into mongodb==========================================================
                    mongodb.insert_many(collection_name="sensor", records=records)
                    records = []
            x = x + 1
        except KeyboardInterrupt:
            break

    consumer.close()
