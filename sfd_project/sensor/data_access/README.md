# Data Collection Phase

This repo help us to know how to publish and consume data to and from kafka confluent in json format.

Step 1: Create a conda environment

```
conda --version
```

Step2: Create a conda environment

```
conda create -n venv python==3.8 -y
```

Step3:

```
conda activate venv
```

Step4:

```
pip install -r requirements.txt
```

### Confluent Kafka Account (on web)

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

  Now, export the environment variables using the following commands:

  ```bash
  export BOOTSTRAP_SERVERS=<CLUSTER_BOOTSTRAP_SERVER>
  export API_KEY=<CLUSTER_API_KEY>
  export API_SECRET=<CLUSTER_API_SECRET>
  export SCHEMA_REGISTRY_API_KEY=<SCHEMA_REGISTRY_API_KEY>
  export SCHEMA_REGISTRY_API_SECRET=<SCHEMA_REGISTRY_API_SECRET>
  export SCHEMA_REGISTRY_ENDPOINT=<SCHEMA_REGISTRY_ENDPOINT_URL>
  ```

### MongoDB

Data base related Environment Variable

```
export MONGO_DB_URL=<MONGO_DB_URL>
```

## Update the credential in .env file and run below command to run your application in docker container

Create .env file in root dir of your project if it is not available
paste the below content and update the credentials

```
API_KEY=asgdakhlsa
API_SECRET_KEY=dsdfsdf
BOOTSTRAP_SERVER=sdfasd
SCHEMA_REGISTRY_API_KEY=sdfsaf
SCHEMA_REGISTRY_API_SECRET=sdfasdf
ENDPOINT_SCHEMA_URL=sdafasf
MONGO_DB_URL=sdfasdfas
```

Build docker image

```
docker build -t data-pipeline:lts .
```

For linux or mac
Run docker image

```
docker run -it -v $(pwd)/logs:/logs  --env-file=$(pwd)/.env data-pipeline:lts
```

## Dataset

You can find full dataset here: [APS Failure at Scania Trucks. (2017). UCI Machine Learning Repository.](https://doi.org/10.24432/C51S51)

Note, I have used only sample of this dataset, for the purpose of this project. You can find the sample dataset in the `data` folder.
