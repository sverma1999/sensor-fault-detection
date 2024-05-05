# **Sensor-fault-detection**

**Current project status:**

```diff
! In Progress
```

## Problem Statement

Modern heavy-duty vehicles utilize Air Pressure Systems (APS), which rely on compressed air instead of hydraulic systems to engage the brake pads. The key advantages of APS include the ease of obtaining compressed air and its long-term sustainability. However, APS-equipped brakes require a continuous supply of compressed air to remain disengaged and allow the vehicle to move. If, due to any unforeseen circumstances, this supply of pressurized air becomes compromised, the brakes fail to disengage, causing the truck to come to a halt. In such situations, truck owners are compelled to dispatch a repair vehicle to diagnose and rectify the malfunction. The challenge lies in the complexity of the APS, which spans both the truck and trailer and consists of an extensive network of pipes responsible for supplying air. This intricacy makes it exceedingly difficult to pinpoint whether the issue stems from the APS or another source. Consequently, fleet owners incur significant expenses in terms of time and money that could otherwise be saved.

Additionally, the APS is equipped with sensors that collect health data about the system. Early detection of APS-related faults could result in substantial time and cost savings by allowing for preemptive repairs. Conversely, if a fault is unrelated to the APS, substantial savings can still be achieved by avoiding unnecessary checkups, along with the associated time and costs. This focused approach allows resources to be channeled effectively to other critical components of the truck, enhancing overall operational efficiency.

- APS is integral to heavy-duty vehicle operation.
- Brake malfunctions stemming from APS issues result in downtime and repair costs.
- Identifying APS-related faults early can lead to substantial cost and time savings.

The Scania dataset encompasses a multitude of features that are used to predict the class of failure. The negative class denotes failures unrelated to the APS, while the positive class signifies failures attributed to the APS.

## Solution Proposed

Introducing a machine learning algorithm/system capable of predicting whether a truck fault is linked to the APS represents a substantial advancement, greatly benefiting all stakeholders by reducing downtime and minimizing breakdown-related expenses. The proposed solution seeks to tackle the challenge of cost minimization within the Air Pressure System (APS) of heavy-duty trucks. This project will employ a binary classification approach to differentiate between failures caused by specific APS components and those originating elsewhere. The primary focus will revolve around minimizing false predictions and, in turn, curbing financial expenditures associated with unnecessary repairs.

- Implementing a machine learning system for fault classification.
- Binary classification approach: APS-related failures vs. other failures.
- Priority on reducing false positive predictions to optimize cost savings.

## Tech Stack Used

1. Python
2. FastAPI
3. Machine learning algorithms
4. Docker
5. MongoDB

## Infrastructure Required.

1. AWS S3
2. AWS EC2
3. AWS ECR
4. Git Actions
5. Terraform

## Before Running the Project

Before we run the project, make sure that you are having MongoDB in your local system, with Compass since we are using MongoDB for data storage. You also need AWS account to access the service like S3, ECR and EC2 instances.

## GitHub workflow is used for CI/CD pipeline



## Data Collections to Endpoints

![image](docs/dataCollection_toEndpoints.png)

### Data Collection

More information about data collection can be found [here](data_collection).

Data collection is done using Kafka and MongoDB.
![image](data_collection/docs/data_collection.png)

## Project Archietecture

![image](https://user-images.githubusercontent.com/57321948/193536768-ae704adc-32d9-4c6c-b234-79c152f756c5.png)

## Deployment Archietecture

Under Construction...

<!--
![image](https://user-images.githubusercontent.com/57321948/193536973-4530fe7d-5509-4609-bfd2-cd702fc82423.png) -->



# Steps to run the project

### Step 1: Clone the repository

  ```bash
  git clone https://github.com/sverma1999/sensor-fault-detection.git
  ```

- Follow rest of steps for [data_collection](data_collection/README.md)
  - Data Collection also has [README.md](data_collection/README.md) file, which contains the steps to run the project, and closer look of the code flow.
<!-- - Follow rest of the steps for [sfd_project](sfd_project/README.md)
  - sfd_project also has [README.md](sfd_project/README.md) file, which contains the steps to run the project, and closer look of the code flow. -->

<!-- # Peek of the High Level Training Pipeline

![image](flowcharts/0_training_pipeline.png) -->

<!-- ## Jump to References

[High Level Code flow chart](sfd_project/flowcharts/0_training_pipeline.png) -->

## Step 2 - Using Docker to run the project (In your local system)
- Make sure you have Docker installed in your machine.
- Start the Docker Desktop application.
- Once start running, run the following commands in the terminal of the project:
  ```bash
    docker build -t sfd_latest .
    docker run -d -p 8080:8080 --name latest_sfd_container sfd_latest
  ```
- Open the browser and go to `http://localhost:8080/` to see the application running.


<!-- 
# For sfd_project folder -->

### Step 2 - Manually running the project (In your local system)

Create a conda environment after opening the repository

```bash
conda create -n sfdVenv python=3.8 -y
```
Activate the environment
```bash
conda activate sfdVenv
```

### Step 3 - Install the requirements

```bash
pip install -r requirements.txt
```

### Step 4 - Export the environment variable

Create `.env` file in root folder and add environment variables in it:

```bash
AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>

AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>

AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>

MONGO_DB_URL="mongodb+srv://<username>:<password>@cluster0.nbka4hq.mongodb.net/test"
```

### Step 5 - Run the application server

```bash
python main.py
```
- This will start the FastAPI server at http://localhost:8080/

  ```bash
  http://localhost:8080/docs
  ```

### Step 6. Train application

```bash
http://localhost:8080/train
```
or

Click on the `Train` button in the FastAPI documentation page.


### Step 7. Prediction application

```bash
http://localhost:8080/predict
```
or

Click on the `Predict` button in the FastAPI documentation page.

## Important folders/files and their meanings

- **config:**
  - **schema.yaml:** This file contains the schema of the input data.
  - **model.yaml:**
- **docs:** This folder contains the documentation of the project in the form of images and markdown files.
- **flowcharts:** This folder contains the flowcharts of the project in the form of images.
- **mlruns:** This folder is created by MLFlow to store the model experiment logs.
- **sensor:** All the code related to the sensor project goes here.
  - **cloud_storage:** Code to manage files across cloud goes here.
  - **components:** For creating independent components of the project, such as data ingestion, data preprocessing, model training, model prediction etc...
  - **configuration:** To maintain the connections related configurations such s3 bucket connection, MongoDB connection.
  - **constant:** Things like file paths, s3 bucket names, database names, model names, environment variables, etc... will stay constant all through the project.
  - **data_access:** The code to get data from MongoDB goes here.
  - **entity:** Defines Structure for input and output of every machine learning component.
    - **artifact_entity:** Describes the output of the training components like data ingestion, data preprocessing etc...
    - **config_entity:** Describes the input configuration of the training components like data ingestion, data preprocessing etc...
  - **ml:** Any custom model, accuracy, loss, graph, feature engineering etc... goes here.
  - **pipeline:** Training and Prediction pipelines goes here.
  - **utils:** Folder to keep all the utility functions.
    - **main_utils.py:** Any simple functions that are used in multiple places goes here.
    - **exception.py:** To handle any abnormal errors.
    - **logger.py:** To keep record of what is happening inside the code.
- **venv(folder unavailable on Git):** Virtual environment for this project with Python==3.8.
- **main.py:** This is the main file to run the application.
- **requirements.txt:** This file lists all the required Python packages and their versions, making it easier to reproduce the project's environment and dependencies.
- **setup.py:** This file is used to define the project's metadata and dependencies, making it easier to distribute and install the project as a Python package.
  - This can be run as `python setup.py install` to install the project as a package.
- **start_experiment.sh:** This is a bash script to run the model experiment with MLFlow.

# Code Flow

## High Level Code Flow of Training Pipeline

![image](flowcharts/0_training_pipeline.png)

## Low Level Code Flow

### Data Ingestion

![image](flowcharts/1_Sensor_Data_Ingestion_Component.png)

### Data Validation

Under Construction...

### Data Transformation

Under Construction...

### Model Training

Under Construction...

### Model Evaluation

Under Construction...

### Model Pusher

Under Construction...

## Acknowledgment

I learned about this project from a course at [Inuerons](https://ineuron.ai/).
