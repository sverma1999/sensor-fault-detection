# dataclass is a decorator which is used to create a class with some special features.
# it is used to create a class with attributes, constructor, and methods.
# no need to use __init__ method or self keyword.
from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    trained_file_path: str

    test_file_path: str


@dataclass
class DataValidationArtifact:
    validation_status: bool

    valid_train_file_path: str

    valid_test_file_path: str

    invalid_train_file_path: str

    invalid_test_file_path: str

    drift_report_file_path: str


@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str

    transformed_train_file_path: str

    transformed_test_file_path: str


@dataclass
class ClassificationMetricArtifact:
    f1_score: float

    precision_score: float

    recall_score: float


@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str

    # # For method 2
    # metric_artifact: ClassificationMetricArtifact

    # For method 1
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact
    model_params: dict
    model: object


# For method 2: Using ModelFactory from neuro_mf package==============================
# @dataclass
# class ModelTrainerArtifact:
#     trained_model_file_path: str

#     metric_artifact: ClassificationMetricArtifact


@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool
    changed_accuracy: float
    best_model_path: str
    best_model_metric_artifact: ClassificationMetricArtifact
    trained_model_path: str
    # shape_plots_dir_path: str
    # train_model_metric_artifact: ClassificationMetricArtifact


# For cloud purpose
@dataclass
class ModelPusherArtifact:
    bucket_name: str
    s3_model_path: str


# # For local purpose
# @dataclass
# class ModelPusherArtifact:
#     saved_model_path: str
#     model_file_path: str
