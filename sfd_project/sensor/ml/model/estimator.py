import sys

from pandas import DataFrame
import numpy as np
from sklearn.pipeline import Pipeline

from sensor.exception_code.exception import SensorException
from sensor.logger_code.logger import logging
from sensor.constant.trainingPipeline_consts import *


# custom class to map the target value to 0 and 1, doing for learning purpose.
# other option is to use LabelEncoder from sklearn.preprocessing
class TargetValueMapping:
    def __init__(self):
        # negative class is mapped to 0 and positive class is mapped to 1
        self.neg: int = 0
        self.pos: int = 1

    # returns the dictionary of class mapping with neg and pos.
    def to_dict(self):
        return self.__dict__

    # returns the dictionary of class mapping with 0 and 1 to neg and pos respectively.
    def reverse_mapping(self):
        mapping_response = self.to_dict()

        return dict(zip(mapping_response.values(), mapping_response.keys()))


class SensorModel:
    def __init__(self, preprocessing_object, trained_model_object):
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    # predicting the target value using the trained model
    def predict(self, test_data_frame: DataFrame) -> np.ndarray:
        logging.info("Entered inside predict method of SensorModel class")
        try:
            logging.info("Using the trained model to get predictions")

            logging.info(
                f"type of preprocessing_object: {type(self.preprocessing_object)}"
            )
            logging.info(
                f"type of trained_model_object: {type(self.trained_model_object)}"
            )

            # test data needs to be transformed using the same preprocessing object used for training
            transformed_feature = self.preprocessing_object.transform(test_data_frame)

            logging.info("Used the trained model to get predictions")

            return self.trained_model_object.predict(transformed_feature)

        except Exception as e:
            raise SensorException(e, sys) from e

    # __repr__  and __str__ are being overridden to print the model name
    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"

    # def is_model_present(self, model_path):
    #     """
    #     Method Name :   is_model_present
    #     Description :   This method checks whether model is present in the bucket or not

    #     :param model_path: Location of your model in bucket

    #     :Output      :   True if model is present else False
    #     On Failure  :   Write an exception log and then return False

    #     Version     :   1.2
    #     Revisions   :   moved setup to cloud
    #     """

    #     logging.info("Entered is_model_present method of SensorEstimator class")
    #     try:
    #         # checking whether model is present in the bucket or not
    #         # true if model is present else false
    #         return self.s3.s3_key_path_available(
    #             bucket_name=self.bucket_name, s3_key=model_path
    #         )

    #     except SensorException as e:
    #         print(e)
    #         logging.info(
    #             "Exception occured in is_model_present method of SensorEstimator class, returned False"
    #         )
    #         return False


class ModelResolver:
    def __init__(self, model_dir=SAVED_MODEL_DIR):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise SensorException(e, sys)

    # get the best model from the model directory: most recently saved model according to time stamp.
    def get_best_model_path(
        self,
    ) -> str:
        logging.info("Entered get_best_model_path method of ModelResolver class")
        try:
            # get the list of time stamps of the saved models
            # time_stamps = list(map(int, os.listdir(self.model_dir)))

            # logging.info(f"Max of time_stamps: {max(os.listdir(self.model_dir))}")

            # logging.info(f"time_stamps: {time_stamps}")

            # get the latest time stamp
            # latest_timeStamp = max(time_stamps)

            latest_timeStamp = max(os.listdir(self.model_dir))

            logging.info(f"latest_timeStamp: {latest_timeStamp}")

            # get the path of the latest model
            latest_model_path = os.path.join(
                self.model_dir, str(latest_timeStamp), MODEL_FILE_NAME
            )

            logging.info(f"latest_model_path: {latest_model_path}")

            return latest_model_path
        except Exception as e:
            raise SensorException(e, sys)

    def is_model_present(self) -> bool:
        logging.info("Entered is_model_present method of ModelResolver class")
        try:
            # check if the model directory exists
            if not os.path.exists(self.model_dir):
                logging.info("Model directory does not exist")
                return False
            # check if the model directory is empty
            time_stamps = os.listdir(self.model_dir)
            if len(time_stamps) == 0:
                logging.info("Model directory is empty")
                return False
            latest_model_path = self.get_best_model_path()
            # logging.info(
            #     f"os.path.exists(latest_model_path): {os.path.exists(latest_model_path)}"
            # )
            if not os.path.exists(latest_model_path):
                logging.info("Latest Model path does not exist")
                return False
            # if none of the of the above conditions are true, then return True
            return True
        except Exception as e:
            raise SensorException(e, sys)
