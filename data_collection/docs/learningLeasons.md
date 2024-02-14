# Lessons Learned from the Data Collection Phase

## Kafka

The Kafka works as mediator between data producer and data consumer. It is like broker system
where many devices can publish/produce data to the Kafka in real-time and many devices or servers can consume data from the Kafka. The Kafka holds the data for some time and then delete it. It is like a distributed database system.

The Kafka is a publish-subscribe based messaging system. It is fast, scalable and durable. It is fault-tolerant and highly available. The Kafka is used for building real-time data pipelines and streaming apps. It is horizontally scalable, fault-tolerant, wicked fast, and runs in production in thousands of companies.

Kafka topics are divided into a number of partitions. Partitions allow you to parallelize a topic by splitting the data in a particular topic across multiple brokers — each partition can be placed on a separate machine to allow for multiple consumers to read from a topic in parallel.

### Example Scenerio

Assume, if there are 4 trucks and each has Air Pressure System (APS), Geographical Positioning System (GPS), and Electrical System (ES). Each system
has its own components along with sensors to collect data.
Since they are three different systems, they will publish data to three different topics.
The data from APS system will be published to APS topic, the data from GPS system will be published to GPS topic, and the data from ES system will be published to IMU topic.

Producers:

- The four trucks are represented as producers. Each truck sends data to the respective topics ("truckX_aps_data," "truckX_gps_data," "truckX_es_data") based on the type of data it is collecting.

Consumers:

- Consumers are applications or services that subscribe to Kafka topics to process data.
- There could be three consumer groups, each processing data from one type of topic (truckX_aps_data, truckX_gps_data, and truckX_imu_data). Each consumer group may have multiple consumer instances.
- Consumers read data from specific partitions within the topics, ensuring parallel processing of data streams.

## Producer

In real-time scenario:

- The data will be collected from the sensors, and then it will be published to the Kafka.
- Code for producer will be running on the device where the sensors are installed.

For this project:

- I have used sample_data `aps_failure_training_set1.csv` file as data source.
- I have used `pandas` library to read the csv file and then converted it into dataframe.
- The sample_data file is useful for schema file to define the structure of data.

## Consumer

In real-time scenario:

- The data will be consumed by the client application from the Kafka to process it further and store it in the database.
- The consumer Code will be running on the server where the client application is installed.
- You will have information about structure of the data, so you can define the schema for the data.

In this project:

- I have used `pyspark` library to consume data from the Kafka. This pyspark application will read data from the Kafka and then process it further to store it in the MongoDB database.
- The consumer code will be running on different terminal window, for one consumer group, you can have multiple consumer instances.
- The sample_data file is useful for schema file to define the structure of data. This sample_data file is same as the data source for producer.
