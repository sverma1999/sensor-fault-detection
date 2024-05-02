import sys

from sensor.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    ModelEvaluationConfig,
    ModelPusherConfig,
    ModelTrainerConfig,
)

from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.model_pusher import ModelPusher

from sensor.entity.artifact_entity import (
    DataIngestionArtifact,
    DataTransformationArtifact,
    DataValidationArtifact,
    ModelEvaluationArtifact,
    ModelTrainerArtifact,
)

from sensor.exception_code.exception import SensorException
from sensor.logger_code.logger import logging

from sensor.constant.s3_bucket import TRAINING_BUCKET_NAME

# from sensor.constant.trainingPipeline_consts import (
#     MODEL_PUSHER_SAVED_MODEL_DIR,
#     MODEL_PUSHER_BUCKET_NAME,
# )
# from sensor.cloud_storage.s3_syncer import S3Sync


class TrainingPipeline:
    is_pipeline_running = False

    def __init__(self):
        # data_ingestion_config to be passed to the DataIngestion component

        # self.training_pipeline_config = TrainingPipelineConfig()

        self.data_ingestion_config = DataIngestionConfig()

        self.data_validation_config = DataValidationConfig()

        self.data_transformation_config = DataTransformationConfig()

        self.model_trainer_config = ModelTrainerConfig()

        self.model_evaluation_config = ModelEvaluationConfig()

        self.model_pusher_config = ModelPusherConfig()

        # self.s3_sync = S3Sync()

    # Feed the data_ingestion_config to the DataIngestion component, and return the DataIngestionArtifact
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info(
                "Entered the start_data_ingestion method of TrainPipeline class"
            )

            # self.data_ingestion_config = DataIngestionConfig(
            #     training_pipeline_config=self.training_pipeline_config
            # )

            # Component 1: DataIngestion, passing the input config
            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )

            # output of the DataIngestion component
            # sensor.csv file will be saved in feature_store directory of the artifact
            # train.csv and test.csv files will be saved in ingested directory of the artifact
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
            # Component 2: DataValidation, passing the input config
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config,
            )

            # output of the DataValidation component
            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation operation")

            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys) from e

    def start_data_transformation(
        self, data_validation_artifact: DataValidationArtifact
    ):
        logging.info(
            "Entered the start_data_transformation method of TrainPipeline class"
        )
        try:
            # Component 3: DataTransformation, passing the input config
            data_transformation = DataTransformation(
                data_validation_artifact, self.data_transformation_config
            )

            # output of the DataTransformation component
            data_transformation_artifact = (
                data_transformation.initiate_data_transformation()
            )

            logging.info("Performed the data transformation operation")
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def start_model_trainer(
        self, data_trasnformation_artifact: DataTransformationArtifact
    ):
        logging.info("Entered the start_model_trainer method of TrainPipeline class")

        try:
            # Component 4: ModelTrainer, passing the input config and the DataTransformationArtifact
            model_trainer = ModelTrainer(
                data_transformation_artifact=data_trasnformation_artifact,
                model_trainer_config=self.model_trainer_config,
            )

            # output of the ModelTrainer component
            model_trainer_artifact = model_trainer.initiate_model_trainer()

            logging.info("Performed the data training operation")
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def start_model_evaluation(
        self,
        data_validation_artifact: DataValidationArtifact,
        model_trainer_artifact: ModelTrainerArtifact,
    ):
        logging.info("Entered the start_model_evaluation method of TrainPipeline class")

        try:
            # Component 5: ModelEvaluation, passing the input config and the DataValidationArtifact and ModelTrainerArtifact
            model_evaluation = ModelEvaluation(
                model_eval_config=self.model_evaluation_config,
                data_validation_artifact=data_validation_artifact,
                model_trainer_artifact=model_trainer_artifact,
            )

            # output of the ModelEvaluation component
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()

            logging.info("Performed the data evaluation operation")

            return model_evaluation_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def start_model_pusher(self, model_trainer_artifact: ModelTrainerArtifact):
        logging.info("Entered the start_model_pusher method of TrainPipeline class")

        try:
            # Component 6: ModelPusher, passing the input config and the ModelEvaluationArtifact
            model_pusher = ModelPusher(
                model_pusher_config=self.model_pusher_config,
                model_trainer_artifact=model_trainer_artifact,
            )

            # output of the ModelPusher component for cloud testing
            model_pusher_artifact = model_pusher.initiate_model_pusher()

            # # output of the ModelPusher component for local testing
            # model_pusher_artifact = model_pusher.initiate_model_pusher_locally()

            logging.info("Performed the data pusher operation")
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e, sys)

    # # This function will sync and automatically upload the artifact directory to the s3 bucket
    # def sync_artifact_dir_to_s3(self):
    #     try:
    #         aws_bucket_url = f"s3://{MODEL_PUSHER_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
    #         self.s3_sync.sync_folder_to_s3(
    #             folder=self.training_pipeline_config.artifact_dir,
    #             aws_bucket_url=aws_bucket_url,
    #         )
    #     except Exception as e:
    #         raise SensorException(e, sys)

    # # This function will sync and automatically upload the saved_model directory to the s3 bucket
    # def sync_saved_model_dir_to_s3(self):
    #     try:
    #         aws_bucket_url = (
    #             f"s3://{MODEL_PUSHER_BUCKET_NAME}/{MODEL_PUSHER_SAVED_MODEL_DIR}"
    #         )
    #         self.s3_sync.sync_folder_to_s3(
    #             folder=MODEL_PUSHER_SAVED_MODEL_DIR, aws_bucket_url=aws_bucket_url
    #         )

    #     except Exception as e:
    #         raise SensorException(e, sys)

    # This function will run the entire training pipeline
    def run_pipeline(
        self,
    ) -> None:
        try:
            TrainingPipeline.is_pipeline_running = True
            # Artifact of the DataIngestion component
            logging.info("Training pipeline started")
            data_ingestion_artifact = self.start_data_ingestion()

            # Artifact of the DataValidation component, reciving the DataIngestionArtifact as input
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact
            )

            # Artifact of the DataTransformation component, reciving the DataValidationArtifact as input
            data_transformation_artifact = self.start_data_transformation(
                data_validation_artifact=data_validation_artifact
            )

            # Artifact of the ModelTrainer component, reciving the DataTransformationArtifact as input
            model_trainer_artifact = self.start_model_trainer(
                data_trasnformation_artifact=data_transformation_artifact
            )

            # Artifact of the ModelEvaluation component, reciving the DataValidationArtifact and ModelTrainerArtifact as input
            model_evaluation_artifact = self.start_model_evaluation(
                data_validation_artifact=data_validation_artifact,
                model_trainer_artifact=model_trainer_artifact,
            )

            # check if the trained model is accepted or not. If not accepted then logg the message and return None
            if not model_evaluation_artifact.is_model_accepted:
                logging.info("Trained model is not better than the best model")
                return None

            # if accepted then push the model
            model_pusher_artifact = self.start_model_pusher(
                model_trainer_artifact=model_trainer_artifact
            )

            TrainingPipeline.is_pipeline_running = False

            logging.info("Training pipeline completed")

            # self.sync_artifact_dir_to_s3()
            # self.sync_saved_model_dir_to_s3()

            # logging.info("Artifact and saved_model directories are synced to s3 bucket")
        except Exception as e:
            # self.sync_artifact_dir_to_s3()
            TrainingPipeline.is_pipeline_running = False
            raise SensorException(e, sys)
