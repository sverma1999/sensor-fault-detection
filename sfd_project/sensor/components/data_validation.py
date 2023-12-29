from sensor.exception_code.exception import SensorException
from sensor.logger_code.logger import logging
from sensor.entity.config_entity import DataValidationConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.data_access.sensor_data import SensorData
from sensor.constant.trainingPipeline_consts import *

from sensor.utils.main_utils import read_yaml_file, write_yaml_file
from sklearn.model_selection import train_test_split
import pandas as pd
import sys, os
import json


class DataValidation:
    def __init__(
        self,
        data_validation_config: DataValidationConfig,
        data_ingestion_artifact: DataIngestionArtifact,
    ):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            # protected variable to store schema config (_ in the start is used to make it protected)
            # keeping it protected becuase we don't want to change it from outside
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            num_of_columns = self._schema_config["columns"]
            if len(dataframe.columns) == num_of_columns:
                return True
            return False
        except Exception as e:
            raise SensorException(e, sys)

    def is_numerical_column_exist(self, dataframe: pd.DataFrame) -> bool:
        try:
            numerical_columns = self._schema_config["numerical_columns"]

            # to get the columns of dataframe
            df_columns = dataframe.columns

            exist = True
            # to keep track of missing columns in dataframe
            missing_columns = []

            # Checking if numerical columns are present in dataframe or not
            for col in numerical_columns:
                if col not in df_columns:
                    exist = False
                    # adding missing column to missing_columns list
                    missing_columns.append(col)
            logging.info(f"Missing columns in dataframe: [{missing_columns}]")
            return exist
        except Exception as e:
            raise SensorException(e, sys)

    # OPTIONAL: Add a method to check if the standard deviation of the numerical columns is zero or not. If it is zero, then it means
    # that the column has only one value and hence it is not useful for training the model. So, we can drop that column.
    # def drop_zero_std_cols(self, dataframe: pd.DataFrame) -> bool:

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e, sys)

    def detect_dataset_drift(self):
        pass

    def initiate_data_validation(self):
        try:
            # ------------------------------------------- Data validation starts here -------------------------------------------

            logging.info("Initiating data validation")

            error_message = ""

            # loading path for train and test file from data_ingestion_artifact (from previouse step of the pipeline)
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Reading the read_data method to read the train and test file
            train_dataframe = DataValidation.read_data(file_path=train_file_path)
            test_dataframe = DataValidation.read_data(file_path=test_file_path)

            # Validate number of columns in train and test file
            # For train data
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"{error_message} Number of columns in train file is not equal to the number of columns in schema file.\n"
            # for test data
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message} Number of columns in test file is not equal to the number of columns in schema file.\n"

            # numerical column validation in train and test file
            # for train data
            status = self.is_numerical_column_exist(dataframe=train_dataframe)
            if not status:
                error_message = f"{error_message} Train dataframe does not have all the numerical columns.\n"
            # for test data
            status = self.is_numerical_column_exist(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message} Test dataframe does not have all the numerical columns.\n"

            if len(error_message) > 0:
                raise Exception(error_message)

            # Data drift detection

            # ------------------------------------------- Data validation ends here -------------------------------------------
        except Exception as e:
            raise SensorException(e, sys)
