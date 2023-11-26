

from sensor.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    # DataTransformationConfig,
    # DataValidationConfig,
    # ModelEvaluationConfig,
    # ModelPusherConfig,
    # ModelTrainerConfig,
)

from sensor.entity.artifact_entity import (
    DataIngestionArtifact,
    # DataTransformationArtifact,
    # DataValidationArtifact,
    # ModelEvaluationArtifact,
    # ModelTrainerArtifact,
)

from sensor.exception import SensorException
from sensor.components.data_ingestion import DataIngestion

from sensor.logger import logging
import sys, os



class TrainingPipeline:
    def __init__(self):

        self.training_pipeline_config = TrainingPipelineConfig()
        
        #self.training_pipeline_config = training_pipeline_config


        # self.data_validation_config = DataValidationConfig()

        # self.data_transformation_config = DataTransformationConfig()

        # self.model_trainer_config = ModelTrainerConfig()

        # self.model_evaluation_config = ModelEvaluationConfig()

        # self.model_pusher_config = ModelPusherConfig()


    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Entered the start_data_ingestion method of TrainPipeline class")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)
        
    def start_data_validation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)
    
    def start_data_transformation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)
        
    def start_model_trainer(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)
        
    def start_model_evaluation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)
        
    def start_model_pusher(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
        except Exception as e:
            raise SensorException(e, sys)
