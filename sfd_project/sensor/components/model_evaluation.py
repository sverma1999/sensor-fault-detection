from sensor.exception_code.exception import SensorException
from sensor.logger_code.logger import logging
from sensor.ml.metric import calculate_metric
from sensor.ml.model.estimator import TargetValueMapping, ModelResolver
from sensor.utils.main_utils import load_object, write_yaml_file
from sensor.constant.trainingPipeline_consts import *
from sensor.entity.config_entity import ModelEvaluationConfig
from sensor.entity.artifact_entity import (
    ClassificationMetricArtifact,
    DataValidationArtifact,
    ModelEvaluationArtifact,
    ModelTrainerArtifact,
)

# from sensor.ml.model.s3_estimator import SensorEstimator
import sys
from typing import Optional

import pandas as pd
from sklearn.metrics import f1_score


class ModelEvaluation:
    def __init__(
        self,
        model_eval_config: ModelEvaluationConfig,
        data_validation_artifact: DataValidationArtifact,
        model_trainer_artifact: ModelTrainerArtifact,
    ):
        try:
            self.model_eval_config = model_eval_config
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        logging.info(
            "Entered initiate_model_evaluation method of ModelEvaluation class"
        )
        try:
            valid_trainFile_path = self.data_validation_artifact.valid_train_file_path
            valid_testFile_path = self.data_validation_artifact.valid_test_file_path

            # laoding training ad trsting data  from valid path
            train_df = pd.read_csv(valid_trainFile_path)
            test_df = pd.read_csv(valid_testFile_path)

            # concatenating both training and testing data, because we need to calculate the metric on both data on trained model and latest model
            df = pd.concat([train_df, test_df])
            logging.info(f"df shape after concat: {df.shape}")

            # true value of the target column
            y_true = df[TARGET_COLUMN]

            y_true.replace(TargetValueMapping().to_dict(), inplace=True)

            # drop the target column from the dataframe
            df.drop(columns=[TARGET_COLUMN], axis=1, inplace=True)

            logging.info(f"df shape after dropping target column: {df.shape}")

            # get the model path from previous artifact (model_trainer_artifact).
            train_model_file_path = self.model_trainer_artifact.trained_model_file_path

            # model resolver object is dfined and to be used to get the best model path
            model_resolver = ModelResolver()

            logging.info("Check model exist or not")
            # if base model is not present, then prepare the output with model_trainer_artifact and return the artifact
            is_model_accepted = True
            logging.info(
                f"model_resolver.does_model_exist(): {model_resolver.does_model_exist()}"
            )
            if not model_resolver.does_model_exist():
                logging.info("Model does not exist")

                model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted,
                    improved_accuracy=None,
                    best_model_path=None,
                    best_model_metric_artifact=None,
                    trained_model_path=train_model_file_path,
                    train_model_metric_artifact=self.model_trainer_artifact.test_metric_artifact,
                )
                logging.info(f"Model trainer artifact: {model_evaluation_artifact}")
                return model_evaluation_artifact

            logging.info("Model already exist")
            # if base model is present, then we have load the latest model
            latest_model_path = model_resolver.get_best_model_path()
            latest_model = load_object(file_path=latest_model_path)

            logging.info("Latest model is the best model so it loaded")

            # load the trained model, which was outputed from model_trainer
            train_model = load_object(file_path=train_model_file_path)

            logging.info("Trained model is loaded")

            # calculate the metric for both trained model and latest model
            trained_metric = calculate_metric(model=train_model, x=df, y=y_true)
            latest_metric = calculate_metric(model=latest_model, x=df, y=y_true)

            logging.info("Metric calculated for both trained and latest model")

            # calculate the improved accuracy, and check if the model is accepted or not based on,
            # if the trained model is better than the latest model: is_model_accepted = True, otherwise is_model_accepted = False
            improved_accuracy = latest_metric.f1_score - trained_metric.f1_score

            logging.info(
                f"Improved accuracy calculated, and it is: {improved_accuracy}"
            )
            if self.model_eval_config.change_threshhold < improved_accuracy:
                logging.info("Trained model is better than the latest model")
                is_model_accepted = True
            else:
                logging.info("Trained model is not better than the latest model")
                is_model_accepted = False

            logging.info("Model evaluation artifact is being prepared")
            # prepare the output artifact with either latest model or trained model
            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=is_model_accepted,
                improved_accuracy=improved_accuracy,
                best_model_path=latest_metric,
                best_model_metric_artifact=latest_metric,
                trained_model_path=train_model_file_path,
                train_model_metric_artifact=trained_metric,
            )

            logging.info("Model evaluation artifact is prepared")

            # write the report
            model_eval_report = model_evaluation_artifact.__dict__
            write_yaml_file(self.model_eval_config.report_file_path, model_eval_report)

            logging.info("Model evaluation report is written")

            logging.info(f"Model trainer artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact

        # model_file_path = self.model_trainer_artifact.model_file_path
        except Exception as e:
            raise SensorException(e, sys)
