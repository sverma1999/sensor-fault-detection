from sensor.exception_code.exception import SensorException
from sensor.logger_code.logger import logging
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.data_access.sensor_data import SensorData

from sklearn.model_selection import train_test_split
from pandas import DataFrame
import sys, os


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SensorException(e, sys)

    def export_data_into_feature_store(self) -> DataFrame:
        """
        Export mongodb collection record as dataframe into feature
        """
        try:
            logging.info("Started exporting data from MongoDB to feature store")

            # creating instance of SensorData class to export data from mongodb
            sensor_data = SensorData()
            # exporting data from mongodb in form of dataframe
            dataframe = sensor_data.export_collection_as_dataframe(
                collection_name=self.data_ingestion_config.collection_name
            )
            # creating path to save the feature store file: sensor.csv
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            # creating folder to save the feature store file
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            # exporting dataframe to feature store file path, sensor.csv, index is false as we don't want to save index column
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise SensorException(e, sys)

    def data_train_test_split(self, dataframe: DataFrame) -> None:
        """
        Feature store dataset will be split into train and test file
        """
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )

            logging.info("Performed train test split on the dataframe")

            logging.info("Exited data_train_test_split method of Data_Ingestion class")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)

            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Exporting train and test file path.")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )

            logging.info(f"Exported train and test file path.")
        except Exception as e:
            raise SensorData(e, sys)

    # Data ingestion component will be initiated from here and call rest of the methods.
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            # exporting data from mongodb to the feature store file (sensor.csv) and return the dataframe
            dataframe = self.export_data_into_feature_store()

            # split the feature store file (sensor.csv) into train and test file
            self.data_train_test_split(dataframe=dataframe)

            # creating instance of DataIngestionArtifact class and return the object of the class with the path of train and test file
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,
            )
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)
