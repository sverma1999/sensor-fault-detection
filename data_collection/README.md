# Data Collection Phase

This repo help us to know how to publish and consume data to and from kafka confluent in json format.

Step 2: Create a conda environment

```
conda create -n venv python==3.8 -y
```

Step 3:

```
conda activate venv
```

Step 4:

```
pip install -r requirements.txt
```

## Confluent Kafka Account (on web)

- I highly recommend following this tutorial: https://github.com/Big-Data-01/confluent-tutorial/tree/main. You can set up account and following required items:

  - Cluster API key
  - Cluster API secret
  - Cluster Bootstrap server
  - Schema Registry API key
  - Schema Registry API secret
  - Schema Registry Endpoint URL

- Set up environment variables in your local machine. You can use the following command to set up environment variables in your local machine:

  <span style="background-color:yellow;"><b>Important note:</b></span>
  Make sure you are exporting these environment variables in the virtual environment you are using for this project. This will ensure that the environment variables are not exposed outside your virtual environment.
  To do that enter command in your terminal:
  <span style="color:green;"><b>conda activate your_virtual_environment</b></span>

  Create `.env` file in root of `data_collection` folder and add environment variables in it:

  ```
  API_KEY=asgdakhlsa
  API_SECRET_KEY=dsdfsdf
  BOOTSTRAP_SERVER=sdfasd
  SCHEMA_REGISTRY_API_KEY=sdfsaf
  SCHEMA_REGISTRY_API_SECRET=sdfasdf
  ENDPOINT_SCHEMA_URL=sdafasf
  ```

  After that import the library `dotenv` and use `load_dotenv()` function to load the environment variables from `.env` file.

## MongoDB

- Create a MongoDB account on web. You can follow this tutorial: https://www.youtube.com/watch?v=rE_bJl2GAY8
- Create a project.
- Create a free cluster.
- Create a database user.
- Add your IP address to the IP access list.
- Connect to your cluster.
- Create a database and collection.
- Get your connection string.

Add connection string to `.env` file:

```
MONGO_DB_URL=mongodb+srv://<username>:<password>@<cluster-url>/<database-name>?retryWrites=true&w=majority
```

Make sure `mongodb.py` file is using the same database name and collection name. My database name was `sensor_readings` and collection name was `sensor`.
My `json_consumer.py` file is using the same collection name.

## Data Collection

![image](docs/data_collection.png)

## Dataset

I have used only sample of this dataset, for the purpose of this project. You can find the sample dataset in the `sample_data` folder.

You can find full dataset here: [APS Failure at Scania Trucks. (2017). UCI Machine Learning Repository.](https://doi.org/10.24432/C51S51)

## Important folders/files and their meanings

- **docs:** All the documentation related to the project goes here.
- **sample_data:** Sample data for the kafka topic.
  - **kafka-sensor-topic:** This folder contains the sample data for kafka topic. It is in-place of real-time data.
    - aps_failure_training_set1.csv
- **src:**
  - **constant:** Things like files, folders, model names etc... will stay constant.
  - **database:** This folder contains all the database related code. For example: mongodb connection, mongodb schema etc...
  - **entity:** This folder contains all the entities related to the project. Functions from here will be used by producer and consumer.
    - **generic.py:** File contains generic functions which can be used by producer and consumer.
  - **kafka_config:** Configuration related to kafka goes here. For example: kafka topic name, kafka bootstrap server, kafka schema registry url etc... This will help producer and consumer to connect to kafka.
  - **kafka_consumer:** This folder contains the code related to kafka consumer.
    - **json_consumer.py:** This file contains the code to consume data from kafka topic and store it in mongodb.
  - **kafka_logger**
  - **kafka_producer:** This folder contains the code related to kafka producer.
    - **json_producer.py:** This file contains the code to publish data to kafka topic.
- **.env:** Environment variables goes here.
- **consumer_main.py:** This file contains the main function for consumer code. Step 1 start from here, and it calls rest of the helper functions to consume data from kafka topic to mongodb.
- **producer_main.py:** This file contains the main function for producer code. Step 1 starts from here, and it calls rest of the helper functions to publish data to kafka topic.
- **requirements.txt:** Contains all the dependencies required for the project.
- **schema.json:** This file contains the schema for the data which will be published to kafka topic.
- **setup.py:** This file contains the code to install the project as a package.
- **start.sh:** This file contains the code to run the project.

## How to run the code

- Step 1: Run the producer code. This will publish data to kafka topic.

  ```
  python producer_main.py
  ```

- Step 2: Open another terminal and activate the same virtual environment.
  - Run the consumer code. This will consume data from kafka topic and store it in mongodb.
    ```
    python consumer_main.py
    ```

Note: Consumer client will keep waiting for the data to be published to kafka topic. So, make sure you run the producer code first and then run the consumer code.

- Monitor the throughput of kafka topic producer and consumer.
- Monitor MongoDB database and collection.
  - Data will be updated in chunks of 5000 records. So, you will see 5000 records at a time in the collection.

## Debugging mode

- In constants folder change the `SAMPLE_DIR`:

```python
SAMPLE_DIR = os.path.join("sensor-fault-detection/data_collection/sample_data")
```

When done debugging, change it back to:

```python
SAMPLE_DIR = os.path.join("sample_data")
```

## To understand the code flow

Jump to the following documentation:

- [Code flow chart](docs/code_flow.md): This flow chart will help you to understand the code flow of the producer and the consumer.
- [Data movement chart](docs/data_movement.md): This flow chart will help you to understand the data movement from the producer to the consumer.
- [Little bit about kafka, producers and consumers](docs/learningLeasons.md): This code will explain you little bit about kafka, producers and consumers.
