from sensor.constant.trainingPipeline_consts import SCHEMA_FILE_PATH
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.entity.config_entity import DataValidationConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import read_yaml_file, write_yaml_file
import pandas as pd
import os, sys
from scipy.stats import ks_2samp


class DataValidation:


    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e, sys)
    
    import pandas as pd

    def drop_zero_standard_deviation_columns(self, dataframe:pd.DataFrame)->pd.DataFrame:
        self.std = dataframe.std(numeric_only=True)
        self.zero_std_cols = self.std[self.std.eq(0)].index.tolist() 
        self.dataframe = dataframe.drop(self.zero_std_cols, axis=1)
        return self.dataframe
        

    def validate_nums_of_colunms(self, dataframe:pd.DataFrame)->bool:
        """
        :param dataframe:
        :return: True if required columns present
        """
        try:
            num_of_dataframe_columns = len(dataframe.columns)
            num_of_schema_config_columns = len(self._schema_config["columns"])
            #status = num_of_dataframe_columns == num_of_schema_config_columns

            logging.info(f"Required dataframe column present: [{num_of_dataframe_columns}]")
            logging.info(f"Required schema_config column present: [{num_of_schema_config_columns}]")
            if num_of_dataframe_columns == num_of_schema_config_columns:
                return True
            return False
            #logging.info(f"Is required column present: [{num_of_columns}]")
            #return num_of_columns
        except Exception as e:
            raise SensorException(e, sys)

    def is_numerical_colunm_exist(self, dataframe: pd.DataFrame)->bool:
        try:
            dataframe_columns = dataframe.columns
            numerical_column_present = True
            numerical_columns = self._schema_config["numerical_columns"]
            missing_numerical_columns = []

            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_column_present = False
                    missing_numerical_columns.append(num_column)

            logging.info(f"Missing numerical column: [{missing_numerical_columns}]")

            return numerical_column_present

        except Exception as e:
            raise SensorException(e, sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e, sys)

    def detect_dataset_drift(self, base_df, current_df, threshold=0.05)->bool:
        try:
            report = {}
            validation_status=True
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_distribution = ks_2samp(d1, d2)
                if threshold <= is_same_distribution.pvalue:
                    drift_found = False
                else:
                    drift_found = True
                    validation_status=False
                report.update({column:{
                    "p_value":float(is_same_distribution.pvalue),
                    "drift_status":drift_found
                }})
                drift_report_file_path = self.data_validation_config.drift_report_file_path

                #create a directory
                dir_path = os.path.dirname(drift_report_file_path)
                os.makedirs(dir_path, exist_ok=True)
                write_yaml_file(file_path=drift_report_file_path, content=report,)
            return validation_status
        except Exception as e:
            raise SensorException(e, sys)
            

    def initiate_data_validation(self)->DataIngestionArtifact:
        try:
            error_message = ""
            logging.info("Starting data validation")

            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            #Reading data from traing and test file path
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            #Validate number of columns
            status = self.validate_nums_of_colunms(dataframe=train_dataframe)
            logging.info(
                f"All required columns present in training dataframe: {status}"
            )
            if not status:
                error_message = f"{error_message} Train dataframe does not contain all columns.\n"

            status = self.validate_nums_of_colunms(dataframe=test_dataframe)
            logging.info(
                f"All required columns present in testing dataframe: {status}"
            )
            if not status:
                error_message = f"{error_message} Test dataframe does not contain all columns.\n"


            #Validate numerical columns

            status = self.is_numerical_colunm_exist(dataframe=train_dataframe)
            if not status:
                error_message=f"{error_message}Train dataframe does not contain all numerical columns"

            status = self.is_numerical_colunm_exist(dataframe=test_dataframe)
            if not status:
                error_message=f"{error_message}Test dataframe does not contain all numerical columns"

            if len(error_message) > 0:
                raise Exception(error_message)
            
            #Drops columns from a Pandas DataFrame that have zero standard deviation.
            train_dataframe = self.drop_zero_standard_deviation_columns(train_dataframe)
            test_dataframe = self.drop_zero_standard_deviation_columns(test_dataframe)

            #Lets check data drift
            drift_status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)

            
            # validation_status = len(error_message) == 0

            # if validation_status:
            #     #Drops columns from a Pandas DataFrame that have zero standard deviation.
            #     train_dataframe = self.drop_zero_standard_deviation_columns(train_dataframe)
            #     test_dataframe = self.drop_zero_standard_deviation_columns(test_dataframe)

            #     #Lets check data drift
            #     drift_status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)

            #     if drift_status:
            #         logging.info(f"Drift detected.")

            # else:
            #     logging.info(f"Validation_error: {error_message}")
            

            data_validation_artifact = DataValidationArtifact(
                validation_status=drift_status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                # invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                # invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact


        except Exception as e:
            raise SensorException(e, sys)