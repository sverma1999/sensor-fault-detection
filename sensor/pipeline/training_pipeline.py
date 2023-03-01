

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

from sensor.logger import logging
import sys, os



class TrainingPipeline:
    def __init__(self):

        training_pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        self.training_pipeline_config = training_pipeline_config


        # self.data_validation_config = DataValidationConfig()

        # self.data_transformation_config = DataTransformationConfig()

        # self.model_trainer_config = ModelTrainerConfig()

        # self.model_evaluation_config = ModelEvaluationConfig()

        # self.model_pusher_config = ModelPusherConfig()


    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Entered the start_data_ingestion method of TrainPipeline class")
            logging.info("Getting the data from mongodb")
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
