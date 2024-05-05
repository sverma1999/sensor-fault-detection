import sys

import numpy as np
import pandas as pd

from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler

from sensor.constant.trainingPipeline_consts import TARGET_COLUMN
from sensor.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact,
)
from sensor.entity.config_entity import DataTransformationConfig
from sensor.exception_code.exception import SensorException
from sensor.logger_code.logger import logging

from sensor.ml.model.estimator import TargetValueMapping
from sensor.utils.main_utils import save_numpy_array_data, save_object


class DataTransformation:
    def __init__(
        self,
        data_validation_artifact: DataValidationArtifact,
        data_transformation_config: DataTransformationConfig,
    ):
        """
        :param data_validation_artifact: Output reference of data validation artifact stage
        :param data_transformation_config: configuration for data transformation
        """
        try:
            self.data_validation_artifact = data_validation_artifact

            self.data_transformation_config = data_transformation_config

        except Exception as e:
            raise SensorException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise SensorException(e, sys)

    # this method is used to transform the data and return pipeline object.
    @classmethod
    def get_data_transformer_object(cls) -> Pipeline:
        """
        :return: Pipeline object to transform dataset
        """
        logging.info(
            "Entered get_data_transformer_object method of DataTransformation class"
        )
        try:
            robust_scaler = RobustScaler()
            simple_imputer = SimpleImputer(strategy="constant", fill_value=0)
            logging.info("Initialized RobustScaler, Simple Imputer")

            preprocessor = Pipeline(
                steps=[
                    ("Imputer", simple_imputer),  # replace missing values with 0
                    (
                        "RobustScaler",
                        robust_scaler,
                    ),  # keep every feature in same range and handle outliers
                ]
            )
            logging.info("Created preprocessor object from ColumnTransformer")
            return preprocessor
        except Exception as e:
            raise SensorException(e, sys) from e

    def initiate_data_transformation(
        self,
    ) -> DataTransformationArtifact:
        try:
            logging.info("Starting data transformation")

            # read the train and test data
            train_df = DataTransformation.read_data(
                self.data_validation_artifact.valid_train_file_path
            )

            test_df = DataTransformation.read_data(
                file_path=self.data_validation_artifact.valid_test_file_path
            )
            # get the preprocessor object
            preprocessor = self.get_data_transformer_object()

            logging.info("Got the preprocessor object")

            # Training dataframe---------
            # drop the target column from train data to create input feature train data
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            # load only target column from train data to create target feature train data
            target_feature_train_df = train_df[TARGET_COLUMN]

            # Use target value mapping class to map the target value to 0 and 1
            target_feature_train_df = target_feature_train_df.replace(
                TargetValueMapping().to_dict()
            )

            logging.info("Got input features and target feature of Training dataset")

            # Testing dataframe---------
            # drop the target column from test data to create input feature test data
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            # load only target column from test data to create target feature test data
            target_feature_test_df = test_df[TARGET_COLUMN]

            # Use target value mapping class to map the target value to 0 and 1
            target_feature_test_df = target_feature_test_df.replace(
                TargetValueMapping().to_dict()
            )

            logging.info("Got input features and target feature of Testing dataset")

            logging.info(
                "Applying preprocessing object on training dataframe and testing dataframe"
            )

            # fit transform the input features of training dataframe
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)

            logging.info(
                "Used the preprocessor object to fit transform the inout features of training dataframe"
            )

            # fit transform the input features of testing dataframe
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)

            logging.info(
                "Used the preprocessor object to transform the input features of testing dataframe"
            )

            logging.info("Applying SMOTETomek on Training dataset")

            # apply SMOTETomek on training dataset
            # minority class is oversampled and majority class is undersampled
            # reminder: SMOTE is used to balance the dataset by oversampling the minority class
            smt = SMOTETomek(sampling_strategy="minority")

            # apply SMOTETomek on training dataset
            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                input_feature_train_arr, target_feature_train_df
            )

            logging.info("Applied SMOTETomek on training dataset")

            logging.info("Applying SMOTETomek on testing dataset")

            # apply SMOTETomek on testing dataset
            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                input_feature_test_arr, target_feature_test_df
            )

            logging.info("Applied SMOTETomek on testing dataset")

            logging.info("Now combine the input and target feature of training dataset")
            # numpy has c_ function to combine the input and target feature of training dataset
            train_arr = np.c_[
                input_feature_train_final, np.array(target_feature_train_final)
            ]
            # numpy has c_ function to combine the input and target feature of testing dataset
            test_arr = np.c_[
                input_feature_test_final, np.array(target_feature_test_final)
            ]

            logging.info("Created train array and test array")

            # Here we will save the preprocessing object as a file using dill, so that we can use it in prediction
            # example: preprocessing_pipeline.pkl
            save_object(
                self.data_transformation_config.transformed_object_file_path,
                preprocessor,
            )
            logging.info("Saved the preprocessor object")

            # For training array: Save the numpy array data to the file path mentioned in config file
            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path,
                array=train_arr,
            )

            # For testing array: Save the numpy array data to the file path mentioned in config file
            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path,
                array=test_arr,
            )

            logging.info("Saved the train array and test array")

            # create the data transformation artifact object
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

            logging.info(
                f"Completed data transformation artifact stage and returning the: {data_transformation_artifact}"
            )
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys) from e
