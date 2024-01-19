from datetime import datetime
import os

# dataclass is a decorator which is used to create a class with some special features.
# it is used to create a class with attributes, constructor, and methods.
# no need to use __init__ method or self keyword.
from dataclasses import dataclass

from sensor.constant.trainingPipeline_consts import *
from sensor.constant.predictionPipeline_consts import *
from sensor.entity.artifact_entity import ClassificationMetricArtifact

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")


@dataclass
class TrainingPipelineConfig:
    pipeline_name: str = PIPELINE_NAME
    artifact_dir: str = os.path.join(ARTIFACT_DIR, TIMESTAMP)
    timestamp: str = TIMESTAMP


training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()


@dataclass
class DataIngestionConfig:
    # path to save feature store file (sensor.csv) and ingested data files (train.csv/test.csv)
    # data_ingestion_dir should contain = artifact/{timestamp}/data_ingestion
    data_ingestion_dir: str = os.path.join(
        training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME
    )

    # feature_store_file_path should contain = artifact/{timestamp}/data_ingestion/feature_store/sensor.csv
    feature_store_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME
    )

    # training_file_path should contain = artifact/{timestamp}/data_ingestion/ingested/train.csv
    training_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME
    )

    # testing_file_path should contain = artifact/{timestamp}/data_ingestion/ingested/test.csv
    testing_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME
    )

    train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATION

    collection_name: str = DATA_INGESTION_COLLECTION_NAME


@dataclass
class DataValidationConfig:
    # path to save validated data files
    data_validation_dir: str = os.path.join(
        training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME
    )

    # path to save valid data files
    valid_data_dir: str = os.path.join(data_validation_dir, DATA_VALIDATION_VALID_DIR)

    # path to save invalid data files
    invalid_data_dir: str = os.path.join(
        data_validation_dir, DATA_VALIDATION_INVALID_DIR
    )

    # path to valid train data file
    valid_train_file_path: str = os.path.join(valid_data_dir, TRAIN_FILE_NAME)

    # path to valid test data file
    valid_test_file_path: str = os.path.join(valid_data_dir, TEST_FILE_NAME)

    # path to invalid train data file
    invalid_train_file_path: str = os.path.join(invalid_data_dir, TRAIN_FILE_NAME)

    # path to invalid test data file
    invalid_test_file_path: str = os.path.join(invalid_data_dir, TEST_FILE_NAME)

    # path to save drift report
    drift_report_file_path: str = os.path.join(
        data_validation_dir,
        DATA_VALIDATION_DRIFT_REPORT_DIR,
        DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
    )


@dataclass
class DataTransformationConfig:
    # directory to save transformed data files
    data_transformation_dir: str = os.path.join(
        training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR_NAME
    )
    # path to save transformed train data file
    transformed_train_file_path: str = os.path.join(
        data_transformation_dir,
        DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
        TRAIN_FILE_NAME.replace("csv", "npy"),
    )

    # path to save transformed test data file
    transformed_test_file_path: str = os.path.join(
        data_transformation_dir,
        DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
        TEST_FILE_NAME.replace("csv", "npy"),
    )

    transformed_object_file_path: str = os.path.join(
        data_transformation_dir,
        DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
        PREPROCSSING_OBJECT_FILE_NAME,
    )


@dataclass
class ModelTrainerConfig:
    # path to the model trainer directory
    model_trainer_dir: str = os.path.join(
        training_pipeline_config.artifact_dir, MODEL_TRAINER_DIR_NAME
    )

    # path to the trained model file
    trained_model_file_path: str = os.path.join(
        model_trainer_dir, MODEL_TRAINER_TRAINED_MODEL_DIR, MODEL_FILE_NAME
    )

    # Accuracy expected from the model
    expected_accuracy: float = MODEL_TRAINER_EXPECTED_SCORE

    # path to the model config file
    model_config_file_path: str = MODEL_TRAINER_MODEL_CONFIG_FILE_PATH

    # For method 1
    overfitting_underfitting_threshold: float = (
        MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD
    )


# @dataclass
# class ModelEvaluationConfig:
#     # path to the model evaluation directory
#     model_evaluation_dir: str = os.path.join(
#         training_pipeline_config.artifact_dir, MODEL_EVALUATION_DIR_NAME
#     )

#     # path to the model evaluation report file, inside the model evaluation directory
#     report_file_path: str = os.path.join(
#         model_evaluation_dir, DATA_EVALUATION_REPORT_NAME
#     )

#     change_threshhold = MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE


@dataclass
class EvaluateModelResponse:
    trained_model_f1_score: float

    best_model_f1_score: float

    is_model_accepted: bool

    changed_accuracy: float

    best_model_metric_artifact: ClassificationMetricArtifact


@dataclass
class ModelEvaluationConfig:
    changed_threshold_score: float = MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE

    bucket_name: str = MODEL_PUSHER_BUCKET_NAME

    s3_model_key_path: str = os.path.join(MODEL_PUSHER_S3_KEY, MODEL_FILE_NAME)


# For local purpose
@dataclass
class ModelPusherConfig:
    model_evaluation_dir: str = os.path.join(
        training_pipeline_config.artifact_dir, MODEL_PUSHER_DIR_NAME
    )
    model_file_path = os.path.join(model_evaluation_dir, MODEL_FILE_NAME)

    saved_model_path = os.path.join(
        SAVED_MODEL_DIR, training_pipeline_config.timestamp, MODEL_FILE_NAME
    )


# # For cloud purpose >>>>>>>>>>>>
# @dataclass
# class ModelPusherConfig:
#     bucket_name: str = MODEL_PUSHER_BUCKET_NAME

#     s3_model_key_path: str = os.path.join(MODEL_PUSHER_S3_KEY, MODEL_FILE_NAME)


# # For cloud purpose >>>>>>>>>>>>
# @dataclass
# class PredictionPipelineConfig:
#     prediction_data_file_name: str = PREDICTION_INPUT_FILE_NAME

#     prediction_output_file_name: str = PREDICTION_OUTPUT_FILE_NAME

#     prediction_data_bucket_name: str = PREDICTION_DATA_BUCKET

#     model_bucket_name: str = MODEL_BUCKET_NAME

#     model_file_path: str = os.path.join(MODEL_PUSHER_S3_KEY, MODEL_FILE_NAME)


# For local testing purpose
@dataclass
class PredictionPipelineConfig:
    prediction_data_file_name: str = LOCAL_PREDICTION_INPUT_FILE_NAME

    prediction_output_file_name: str = LOCAL_PREDICTION_OUTPUT_FILE_NAME

    prediction_data_bucket_name: str = LOCAL_PREDICTION_DATA_BUCKET

    model_bucket_name: str = LOCAL_MODEL_BUCKET_NAME

    model_file_path = os.path.join(
        SAVED_MODEL_DIR, training_pipeline_config.timestamp, MODEL_FILE_NAME
    )
