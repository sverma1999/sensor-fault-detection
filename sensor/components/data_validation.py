from sensor.exception_code.exception import SensorException
from sensor.logger_code.logger import logging
from sensor.entity.config_entity import DataValidationConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.data_access.sensor_data import SensorData
from sensor.constant.trainingPipeline_consts import SCHEMA_FILE_PATH

from sensor.utils.main_utils import read_yaml_file, write_yaml_file

# Profile and DataDriftProfileSection are classes used for creating and visualizing data drift profiles,
# which help you understand how the statistical properties of your data change over time or across different datasets
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection

# from sklearn.model_selection import train_test_split

# from scipy.stats import ks_2samp
# from evidently.model.dashboard import Profile


import pandas as pd
import sys, os
import json


class DataValidation:
    def __init__(
        self,
        data_validation_config: DataValidationConfig,
        data_ingestion_artifact: DataIngestionArtifact,
    ):
        """
        :param data_validation_config: configuration for data validation
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        """
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            # protected variable to store schema config (_ in the start is used to make it protected)
            # keeping it protected becuase we don't want to change it from outside
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        """

        :param dataframe:
        :return: True if required columns present
        """
        try:
            num_of_columns = len(self._schema_config["columns"])
            logging.info(f"Number of columns in schema file: {num_of_columns}")
            logging.info(f"Number of columns in dataframe: {len(dataframe.columns)}")
            if len(dataframe.columns) == num_of_columns:
                return True
            return False
        except Exception as e:
            raise SensorException(e, sys)

    def is_numerical_column_exist(self, dataframe: pd.DataFrame) -> bool:
        """
        This function check numerical column is present in dataframe or not
        :param dataframe:
        :return: True if all column presents else False
        """
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
    # Currently not using it!
    def drop_zero_standard_deviation_columns(
        self, dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        # getting the standard deviation of numerical columns
        self.std = dataframe.std(numeric_only=True)

        # getting the columns with standard deviation equal to zero
        self.zero_std_cols = self.std[self.std.eq(0)].index.tolist()

        # dropping the columns with standard deviation equal to zero
        self.dataframe = dataframe.drop(self.zero_std_cols, axis=1)
        return self.dataframe

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e, sys)

    # # Manual data drift detection using ks_2samp
    # def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
    #     """
    #     This method is used for manual data drift detection
    #     :param base_df: base dataframe
    #     :param current_df: current dataframe
    #     :return: True if drift detected else false
    #     """
    #     try:
    #         # dictionary to store
    #         report = {}
    #         # validation status to keep track of validation
    #         status = True

    #         # For each column, we perform a two-sample Kolmogorov-Smirnov test to determine if the two samples are drawn from the same distribution.
    #         for column in base_df.columns:
    #             # comparing the distribution of one column of base_df and current_df
    #             d1 = base_df[column]
    #             d2 = current_df[column]
    #             is_same_distribution = ks_2samp(d1, d2)

    #             # if p-value is less than threshold, then drift is detected
    #             if threshold <= is_same_distribution.pvalue:
    #                 drift_found = False
    #             else:
    #                 drift_found = True
    #                 # if drift is detected, then validation_status is set to False to indicate that drift is detected
    #                 status = False
    #             # updating the report dictionary with p-value and drift status
    #             report.update(
    #                 {
    #                     column: {
    #                         "p_value": float(is_same_distribution.pvalue),
    #                         "drift_status": drift_found,
    #                     }
    #                 }
    #             )

    #         # Getting the path of drift report file
    #         drift_report_file_path = self.data_validation_config.drift_report_file_path

    #         # create a directory of drift report file if it does not exist
    #         dir_path = os.path.dirname(drift_report_file_path)
    #         os.makedirs(dir_path, exist_ok=True)

    #         # Write the report dictionary to drift report file
    #         write_yaml_file(
    #             file_path=drift_report_file_path,
    #             content=report,
    #         )
    #         # return if the drift is detected or not: True if drift is not detected, False if drift is detected
    #         return status
    #     except Exception as e:
    #         raise SensorException(e, sys) from e

    def detect_dataset_drift(
        self,
        base_df: pd.DataFrame,
        current_df: pd.DataFrame,
    ) -> bool:
        """
        :param base_df: base dataframe
        :param current_df: current dataframe
        :return: True of drift detected else false
        """
        logging.info("Data drift detection starting")
        try:
            # Profile is a container class for organizing various analysis sections,
            # and DataDriftProfileSection is a specific section within Profile used
            # for detecting and visualizing data drift between datasets.
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])
            data_drift_profile.calculate(base_df, current_df)

            logging.info("Data drift calculation completed")

            report = data_drift_profile.json()

            logging.info("Report generated in JSON format")

            json_report = json.loads(report)

            write_yaml_file(
                file_path=self.data_validation_config.drift_report_file_path,
                content=json_report,
            )

            logging.info("Report saved in YAML format")

            # getting the total number of features
            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]

            # getting the number of drifted features
            n_drifted_features = json_report["data_drift"]["data"]["metrics"][
                "n_drifted_features"
            ]

            logging.info(
                f"Number of features: {n_features} and number of drifted features: {n_drifted_features}"
            )
            logging.info(f"{n_drifted_features}/{n_features} drift detected.")

            drift_status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]

            return drift_status

        except Exception as e:
            raise SensorException(e, sys) from e

    def initiate_data_validation(self):
        """
        Method Name :   initiate_data_validation
        Description :   This method initiates the data validation component for the pipeline

        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
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

            logging.info("Train and test data loaded for validation")

            # Validate number of columns in train and test file
            # For train data
            status = self.validate_number_of_columns(dataframe=train_dataframe)

            logging.info(
                f"All required columns present in training dataframe: {status}"
            )
            if not status:
                error_message += f"{error_message} Number of columns in train file is not equal to the number of columns in schema file.\n"

            # for test data
            status = self.validate_number_of_columns(dataframe=test_dataframe)

            logging.info(
                f"All required columns present in training dataframe: {status}"
            )

            if not status:
                error_message += f"{error_message} Number of columns in test file is not equal to the number of columns in schema file.\n"

            # numerical column validation in train and test file
            # for train data
            status = self.is_numerical_column_exist(dataframe=train_dataframe)

            logging.info(
                f"Numerical columns are missing in training dataframe: {status}"
            )

            if not status:
                error_message += f"{error_message} Train dataframe does not have all the numerical columns.\n"
            # for test data
            status = self.is_numerical_column_exist(dataframe=test_dataframe)

            logging.info(
                f"Numerical columns are missing in testing dataframe: {status}"
            )

            if not status:
                error_message += f"{error_message} Test dataframe does not have all the numerical columns.\n"

            validation_status = len(error_message) == 0

            # Will chaeck if the validation status is true, then only we will check for drift
            if validation_status:
                # Checking for data drift
                drift_status = self.detect_dataset_drift(
                    base_df=train_dataframe,
                    current_df=test_dataframe,
                )
                if drift_status:
                    logging.info(f"Drift detected.")
            else:
                logging.info(f"Validation_error: {error_message}")

            # if len(error_message) > 0:
            #     raise Exception(error_message)

            # Drops columns from a Pandas DataFrame that have zero standard deviation.
            # train_dataframe = self.drop_zero_standard_deviation_columns(train_dataframe)
            # test_dataframe = self.drop_zero_standard_deviation_columns(test_dataframe)

            # Lest check the data drift
            # Not raising exception if drift is detected, becuase we want to continue the pipeline even if drift is detected,
            # and we check the accuracy achived is fine or not. There is only distribution drift. May be if we train the model
            # on the new data, we can get better accuracy.

            # note, We do not need to create another train and test file for invalid data, becuase we are not going to use
            # invalid data for training the model. We are just going to use it for analysis purpose.
            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact
            # ------------------------------------------- Data validation ends here -------------------------------------------
        except Exception as e:
            raise SensorException(e, sys) from e
