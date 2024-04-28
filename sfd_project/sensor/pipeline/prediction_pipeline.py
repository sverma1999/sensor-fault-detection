import sys, os

import numpy as np
import pandas as pd
import pickle
from pandas import DataFrame

from sensor.exception_code.exception import SensorException
from sensor.logger_code.logger import logging
from sensor.utils.main_utils import read_yaml_file, load_object
from sensor.constant.trainingPipeline_consts import SCHEMA_FILE_PATH, TARGET_COLUMN

from sensor.entity.config_entity import (
    PredictionPipelineConfig,
    DataTransformationConfig,
    ModelPusherConfig,
)

# # For local testing purpose >>>>>>>>>>>>>>>>>>>>
# from sensor.ml.model.estimator import TargetValueMapping, ModelResolver


# Cloud imports
from sensor.cloud_storage.aws_storage import SimpleStorageService
from sensor.ml.model.s3_estimator import SensorEstimator
from sensor.ml.model.estimator import TargetValueMapping


class PredictionPipeline:
    # For cloud purpose  >>>>>>>>>>>>>>>>>>>
    def __init__(self) -> None:
        try:
            self.prediction_pipeline_config = PredictionPipelineConfig()

            self.s3_storage = SimpleStorageService()

            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e, sys)

    # # For local testing purpose
    # def __init__(self) -> None:
    #     try:
    #         self.prediction_pipeline_config = PredictionPipelineConfig()
    #         # self.dataTransformation_config = DataTransformationConfig()
    #         self.model_pusher_config = ModelPusherConfig()
    #         self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
    #     except Exception as e:
    #         raise SensorException(e, sys)

    # For cloud purpose >>>>>>>>>>>>>>>>>>>>
    def predict(self, dataframe) -> np.ndarray:
        logging.info("Entered predict method of PredictionPipeline class")
        try:
            model = SensorEstimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path,
            )

            logging.info("Done with the predict method of PredictionPipeline class")
            logging.info("Returning the predicted array")
            return model.predict(dataframe)
        except Exception as e:
            raise SensorException(e, sys)

    # For cloud purpose >>>>>>>>>>>>>>>>>>>>
    def getData(self) -> DataFrame:
        logging.info("Entered inside getData method of PredictionPipeline class")
        try:
            # read the prediction input data file
            prediction_df = self.s3_storage.read_csv(
                filename=self.prediction_pipeline_config.prediction_data_file_name,
                bucket_name=self.prediction_pipeline_config.prediction_data_bucket_name,
            )

            logging.info("Done reading the prediction data file")

            # drop the columns which are not required for prediction, if there are any
            # if self.schema_config["drop_columns"] in prediction_df.columns:
            #     prediction_df = prediction_df.drop(
            #         self.schema_config["drop_columns"], axis=1
            #     )
            for col in self.schema_config["drop_columns"]:
                if col in prediction_df.columns:
                    prediction_df = prediction_df.drop(col, axis=1)
            if TARGET_COLUMN in prediction_df.columns:
                prediction_df = prediction_df.drop(TARGET_COLUMN, axis=1)

            logging.info("Dropped the required columns")

            logging.info("Done with the getData method of PredictionPipeline class")

            return prediction_df

        except Exception as e:
            raise SensorException(e, sys)

    # # For local testing purpose
    # def predict_locally(self, dataframe) -> np.ndarray:
    #     logging.info("Entered predict method of PredictionPipeline class")
    #     try:
    #         # preprocessing_object = load_object(file_path=ss)
    #         # model_object = load_object(
    #         #     file_path=self.prediction_pipeline_config.model_file_path
    #         # )
    #         # model_path = self.model_pusher_config.saved_model_path
    #         # model = load_object(file_path=model_path)
    #         model_resolver = ModelResolver()
    #         latest_model_path = model_resolver.get_best_model_path()

    #         logging.info(f"latest_model_path: {latest_model_path}")

    #         # Open the .pkl file in binary read mode
    #         with open(latest_model_path, "rb") as file:
    #             # Use pickle.load() to deserialize the object from the file
    #             model = pickle.load(file)

    #         # load the model object using pickle library
    #         # model = pickle.loads(latest_model_path)

    #         logging.info("Done with the predict method of PredictionPipeline class")
    #         logging.info("Returning the predicted array")
    #         logging.info(f"model: {model}")
    #         logging.info(f"type of model: {type(model)}")

    #         return model.predict(dataframe)
    #     except Exception as e:
    #         raise SensorException(e, sys)

    # # For local testing purpose
    # def getData_locally(self) -> DataFrame:
    #     logging.info("Entered inside getData method of PredictionPipeline class")
    #     try:
    #         input_data_path = os.path.join(
    #             self.prediction_pipeline_config.prediction_data_bucket_name,
    #             self.prediction_pipeline_config.prediction_data_file_name,
    #         )
    #         logging.info(
    #             f"Done reading the prediction data file from path: {input_data_path}"
    #         )

    #         logging.info(
    #             f"input_data_path: {input_data_path}, which is made of {self.prediction_pipeline_config.prediction_data_bucket_name}, and {self.prediction_pipeline_config.prediction_data_file_name}"
    #         )
    #         # read the prediction input data file
    #         prediction_df = pd.read_csv(input_data_path)

    #         logging.info("Done reading the prediction data file")

    #         # drop the columns which are not required for prediction, if there are any
    #         # if self.schema_config["drop_columns"] in prediction_df.columns:
    #         #     prediction_df = prediction_df.drop(
    #         #         self.schema_config["drop_columns"], axis=1
    #         #     )
    #         for col in self.schema_config["drop_columns"]:
    #             if col in prediction_df.columns:
    #                 prediction_df = prediction_df.drop(col, axis=1)
    #         if TARGET_COLUMN in prediction_df.columns:
    #             prediction_df = prediction_df.drop(TARGET_COLUMN, axis=1)

    #         logging.info("Dropped the required columns")

    #         logging.info("Done with the getData method of PredictionPipeline class")

    #         return prediction_df

    #     except Exception as e:
    #         raise SensorException(e, sys)

    # # For local testing purpose
    # def run_pipeline_locally(self) -> None:
    #     logging.info("Entered run_pipeline method of PredictionPipeline class")
    #     try:
    #         # get the data to be predicted
    #         data_frame = self.getData_locally()

    #         logging.info("Loaded the data to be predicted")

    #         # predict the target value
    #         predicted_array = self.predict_locally(data_frame)

    #         logging.info("Predicted the target value")

    #         # convert the predicted array to dataframe
    #         prediction = pd.DataFrame(list(predicted_array))

    #         logging.info("Converted the predicted array to dataframe")

    #         # rename the column name to class
    #         prediction.columns = ["class"]

    #         logging.info("Renamed the column name to class")

    #         # replace the target value with the actual class name
    #         prediction.replace(TargetValueMapping().reverse_mapping(), inplace=True)

    #         logging.info("Replaced the target value with the actual class name")

    #         # concatenate the predicted dataframe with the original dataframe
    #         predicted_dataframe = pd.concat([data_frame, prediction], axis=1)

    #         logging.info(
    #             "Concatenated the predicted dataframe with the original dataframe"
    #         )

    #         output_data_path = os.path.join(
    #             self.prediction_pipeline_config.prediction_data_bucket_name,
    #             self.prediction_pipeline_config.prediction_output_file_name,
    #         )
    #         # save the predicted dataframe to the local output file as csv
    #         predicted_dataframe.to_csv(output_data_path)

    #         logging.info(
    #             f"Uploaded predicted file locally to: {self.prediction_pipeline_config.prediction_data_bucket_name}"
    #         )

    #         # logging.info(
    #         #     f"File has uploaded to s3 bucket named: {self.prediction_pipeline_config.prediction_data_bucket_name}"
    #         # )

    #     except Exception as e:
    #         raise SensorException(e, sys)

    # For cloud purpose >>>>>>>>>>>>>>>>>>>>
    def run_pipeline(self) -> None:
        logging.info("Entered run_pipeline method of PredictionPipeline class")
        try:
            # get the data to be predicted
            data_frame = self.getData()

            logging.info("Loaded the data to be predicted")

            # predict the target value
            predicted_array = self.predict(data_frame)

            logging.info("Predicted the target value")

            # convert the predicted array to dataframe
            prediction = pd.DataFrame(list(predicted_array))

            logging.info("Converted the predicted array to dataframe")

            # rename the column name to class
            prediction.columns = ["class"]

            logging.info("Renamed the column name to class")

            # replace the target value with the actual class name
            prediction.replace(TargetValueMapping().reverse_mapping(), inplace=True)

            logging.info("Replaced the target value with the actual class name")

            # concatenate the predicted dataframe with the original dataframe
            predicted_dataframe = pd.concat([data_frame, prediction], axis=1)

            logging.info(
                "Concatenated the predicted dataframe with the original dataframe"
            )

            # write/upload the predicted dataframe to the output file in s3 bucket
            self.s3_storage.upload_df_as_csv(
                predicted_dataframe,
                self.prediction_pipeline_config.prediction_output_file_name,
                self.prediction_pipeline_config.prediction_output_file_name,
                self.prediction_pipeline_config.prediction_data_bucket_name,
            )

            logging.info("Uploaded predicted file to s3 bucket_name")

            logging.info(
                f"File has uploaded to s3 bucket named: {self.prediction_pipeline_config.prediction_data_bucket_name}"
            )

        except Exception as e:
            raise SensorException(e, sys)
