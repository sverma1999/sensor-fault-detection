import sys

from sensor.entity.config_entity import (
    DataIngestionConfig,
    # DataTransformationConfig,
    DataValidationConfig,
    # ModelEvaluationConfig,
    # ModelPusherConfig,
    # ModelTrainerConfig,
)

from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation

from sensor.entity.artifact_entity import (
    DataIngestionArtifact,
    # DataTransformationArtifact,
    DataValidationArtifact,
    # ModelEvaluationArtifact,
    # ModelTrainerArtifact,
)

from sensor.exception_code.exception import SensorException
from sensor.logger_code.logger import logging


class TrainingPipeline:
    def __init__(self):
        # data_ingestion_config to be passed to the DataIngestion component
        self.data_ingestion_config = DataIngestionConfig()

        self.data_validation_config = DataValidationConfig()

        # self.data_transformation_config = DataTransformationConfig()

        # self.model_trainer_config = ModelTrainerConfig()

        # self.model_evaluation_config = ModelEvaluationConfig()

        # self.model_pusher_config = ModelPusherConfig()

    # Feed the data_ingestion_config to the DataIngestion component, and return the DataIngestionArtifact
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info(
                "Entered the start_data_ingestion method of TrainPipeline class"
            )

            # self.data_ingestion_config = DataIngestionConfig(
            #     training_pipeline_config=self.training_pipeline_config
            # )

            # Component 1: DataIngestion
            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )

            # output of the DataIngestion component
            # sensor.csv file will be saved in feature store directory of the artifact
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(
                f"Data ingestion completed and artifact: {data_ingestion_artifact}"
            )
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys) from e

    def start_data_validation(
        self, data_ingestion_artifact: DataIngestionArtifact
    ) -> DataValidationArtifact:
        logging.info("Entered the start_data_validation method of TrainPipeline class")
        try:
            # Component 2: DataValidation
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config,
            )

            # output of the DataValidation component
            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation operation")

            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)

    # def start_data_transformation(self):
    #     try:
    #         pass
    #     except Exception as e:
    #         raise SensorException(e, sys)

    # def start_model_trainer(self):
    #     try:
    #         pass
    #     except Exception as e:
    #         raise SensorException(e, sys)

    # def start_model_evaluation(self):
    #     try:
    #         pass
    #     except Exception as e:
    #         raise SensorException(e, sys)

    # def start_model_pusher(self):
    #     try:
    #         pass
    #     except Exception as e:
    #         raise SensorException(e, sys)

    # This method will run the entire training pipeline
    def run_pipeline(
        self,
    ) -> None:
        try:
            # Artifact of the DataIngestion component
            logging.info("Training pipeline started")
            data_ingestion_artifact = self.start_data_ingestion()

            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact
            )
            logging.info("Training pipeline completed")
        except Exception as e:
            raise SensorException(e, sys)
