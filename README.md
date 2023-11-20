# **Sensor-fault-detection**

**Current project status:**
```diff
! In Progress
```
## Problem Statement

This project focuses on binary classification for identifying failures in the Air Pressure System (APS) of heavy-duty vehicles, which use compressed air instead of hydraulic systems to provide pressure to the brake pads. The affirmative class indicates that the failure was caused by a certain component of the APS.

## Solution Proposed

The proposed solution aims to address the issue of minimizing unnecessary repair costs in the Air Pressure system (APS) of heavy-duty trucks. The project will use a binary classification approach to classify the failures as either being related to a specific APS component or some other component. The focus will be on reducing false predictions and minimizing costs.

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

## How to run?

Before we run the project, make sure that you are having MongoDB in your local system, with Compass since we are using MongoDB for data storage. You also need AWS account to access the service like S3, ECR and EC2 instances.

## Data Collections

![image](https://user-images.githubusercontent.com/57321948/193536736-5ccff349-d1fb-486e-b920-02ad7974d089.png)

## Project Archietecture

![image](https://user-images.githubusercontent.com/57321948/193536768-ae704adc-32d9-4c6c-b234-79c152f756c5.png)

## Deployment Archietecture

![image](https://user-images.githubusercontent.com/57321948/193536973-4530fe7d-5509-4609-bfd2-cd702fc82423.png)

### Step 1: Clone the repository

```bash
git clone https://github.com/sverma1999/sensor-fault-detection.git
```

### Step 2- Create a conda environment after opening the repository

```bash
conda create -n sfDetectionVenv python=3.8 -y
```

```bash
conda activate sfDetectionVenv
```

### Step 3 - Install the requirements

```bash
pip install -r requirements.txt
```

### Step 4 - Export the environment variable

```bash
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>

export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>

export AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>

export MONGO_DB_URL="mongodb+srv://<username>:<password>@cluster0.nbka4hq.mongodb.net/test"

```

### Step 5 - Run the application server

```bash
python app.py
```

### Step 6. Train application

```bash
http://localhost:8080/train

```

### Step 7. Prediction application

```bash
http://localhost:8080/predict

```

## Important folders/files and their meanings

- **sensor:** All the code related to the sensor project goes here.
  - **cloud_storage:** Code to manage files across cloud goes here.
  - **components:** For creating machine learning components.
  - **configuration:** To maintain the connections related configurations such s3 bucket connection, MongoDB connection.
  - **constant:** Things like files, folders, model names etc... will stay constant.
  - **data_access:** The code to get data from MongoDB goes here.
  - **entity:** Defines Structure for input and output of every machine learning component.
  - **ml:** Any custom model, accuracy, graph, feature engineering etc... goes here.
  - **pipeline:** Training and Prediction pipelines goes here.
    - **exception.py:** To handle any abnormal errors.
    - **logger.py:** To keep record of what is happening inside the code.
- **venv(folder unavailable on Git):** Virtual environment for this project with Python==3.8.
- **requirements.txt:** This file lists all the required Python packages and their versions, making it easier to reproduce the project's environment and dependencies.
- **setup.py:** This file is used to define the project's metadata and dependencies, making it easier to distribute and install the project as a Python package.

## Acknowledgment
I learned about this project from a course at [Inuerons](https://ineuron.ai/).
