import sys, os

from sensor.entity.artifact_entity import (
    ModelPusherArtifact,
    ModelTrainerArtifact,
    ModelEvaluationArtifact,
)
from sensor.entity.config_entity import ModelPusherConfig
from sensor.exception_code.exception import SensorException
from sensor.logger_code.logger import logging
from sensor.ml.model.s3_estimator import SensorEstimator
import shutil


class ModelPusher:
    # # For local testing purpose
    # def __init__(
    #     self,
    #     model_trainer_artifact: ModelTrainerArtifact,
    #     model_pusher_config: ModelPusherConfig,
    # ):
    #     self.model_trainer_artifact = model_trainer_artifact

    #     self.model_pusher_config = model_pusher_config

    # For cloud purpose
    def __init__(
        self,
        model_trainer_artifact: ModelTrainerArtifact,
        model_pusher_config: ModelPusherConfig,
    ):
        self.model_trainer_artifact = model_trainer_artifact

        self.model_pusher_config = model_pusher_config

        self.sensor_estimator = SensorEstimator(
            bucket_name=model_pusher_config.bucket_name,
            model_path=model_pusher_config.s3_model_key_path,
        )

    # For cloud purpose
    def initiate_model_pusher(self) -> ModelPusherArtifact:
        logging.info("Entered initiate_model_pusher method of ModelTrainer class")

        try:
            logging.info("Uploading artifacts folder to s3 bucket")

            # This will upload the trained model to s3 bucket
            self.sensor_estimator.save_model(
                from_file=self.model_trainer_artifact.trained_model_file_path
            )

            # prepare model pusher artifact
            model_pusher_artifact = ModelPusherArtifact(
                bucket_name=self.model_pusher_config.bucket_name,
                s3_model_path=self.model_pusher_config.s3_model_key_path,
            )

            logging.info("Uploaded artifacts folder to s3 bucket")

            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")

            logging.info("Exited initiate_model_pusher method of ModelTrainer class")

            return model_pusher_artifact

        except Exception as e:
            raise SensorException(e, sys) from e

    # # For local testing purpose
    # def initiate_model_pusher_locally(self) -> ModelPusherArtifact:
    #     logging.info("Entered initiate_model_pusher method of ModelPusher class")
    #     try:
    #         # trained_model_path = self.model_eval_artifact.trained_model_path
    #         trained_model_path = self.model_trainer_artifact.trained_model_file_path
    #         # we will copy trained model to two places

    #         # this is for training pipeline purpose, so we can pull for there.
    #         # model_pusher_config.model_file_path coming from model_evaluation_dir + MODEL_FILE_NAME path.
    #         model_file_path = self.model_pusher_config.model_file_path
    #         os.makedirs(os.path.dirname(model_file_path), exist_ok=True)
    #         # shutil.copy will copy the trained model to model_file_path
    #         shutil.copy(src=trained_model_path, dst=model_file_path)

    #         logging.info(f"{trained_model_path} copied to {model_file_path}")

    #         # save model dir for production purposes
    #         saved_model_path = self.model_pusher_config.saved_model_path
    #         os.makedirs(os.path.dirname(saved_model_path), exist_ok=True)
    #         # shutil.copy will copy the trained model to saved_model_path
    #         shutil.copy(src=trained_model_path, dst=saved_model_path)

    #         logging.info(f"{trained_model_path} copied to {saved_model_path}")

    #         # prepare model pusher artifact
    #         model_pusher_artifact = ModelPusherArtifact(
    #             saved_model_path=saved_model_path, model_file_path=model_file_path
    #         )

    #         logging.info(f"model_pusher_artifact: {model_pusher_artifact}")
    #         return model_pusher_artifact
    #     except Exception as e:
    #         raise SensorException(e, sys)
