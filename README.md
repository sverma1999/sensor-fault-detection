# **Sensor-fault-detection**

## Problem Statement

This project focuses on binary classification for identifying failures in the Air Pressure System (APS) of heavy-duty vehicles, which use compressed air instead of hydraulic systems to provide pressure to the brake pads. The affirmative class indicates that the failure was caused by a certain component of the APS.

## Solution Proposed

The proposed solution aims to address the issue of minimizing unnecessary repair costs in the Air Pressure system (APS) of heavy-duty trucks. The project will use a binary classification approach to classify the failures as either being related to a specific APS component or some other component. The focus will be on reducing false predictions and minimizing costs.

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
