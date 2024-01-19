import sys

from pandas import DataFrame

from sensor.cloud_storage.aws_storage import SimpleStorageService
from sensor.exception_code.exception import SensorException
from sensor.ml.model.estimator import SensorModel
from sensor.logger_code.logger import logging


class SensorEstimator:
    """
    This class is used to save and retrieve sensor model in s3 bucket and to do prediction
    """

    def __init__(self, bucket_name, model_path):
        """
        :param bucket_name: Name of your model bucket
        :param model_path: Location of your model in bucket
        """
        self.bucket_name = bucket_name
        self.s3 = SimpleStorageService()

        self.model_path = model_path
        self.loaded_model: SensorModel = None

    def is_model_present(self, model_path):
        """
        Method Name :   is_model_present
        Description :   This method checks whether model is present in the bucket or not

        :param model_path: Location of your model in bucket

        :Output      :   True if model is present else False
        On Failure  :   Write an exception log and then return False

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """

        logging.info("Entered is_model_present method of SensorEstimator class")
        try:
            # checking whether model is present in the bucket or not
            # true if model is present else false
            return self.s3.s3_key_path_available(
                bucket_name=self.bucket_name, s3_key=model_path
            )

        except SensorException as e:
            print(e)
            logging.info(
                "Exception occured in is_model_present method of SensorEstimator class, returned False"
            )
            return False

    def load_model(
        self,
    ) -> SensorModel:
        """
        Method Name :   load_model
        Description :   This method loads the model from the s3 bucket

        Output      :   return the loaded model

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """

        logging.info("Entered load_model method of SensorEstimator class")

        # Use the helper methods from the SimpleStorageService class to load the model from the bucket
        return self.s3.load_model(self.model_path, bucket_name=self.bucket_name)

    def save_model(self, from_file, remove: bool = False) -> None:
        """
        Method Name :   save_model
        Description :   Save the model to the model_path

        :param from_file: Your local system model path
        :param remove: By default it is false that mean you will have your model locally available in your system folder

        :Output      :   return None, if model is saved successfully
        On Failure  :   Write an exception log and then return None

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered save_model method of SensorEstimator class")
        try:
            # Use the helper methods from the SimpleStorageService class to upload the model file to the bucket
            self.s3.upload_file(
                from_file,
                to_filename=self.model_path,
                bucket_name=self.bucket_name,
                remove=remove,
            )

        except Exception as e:
            raise SensorException(e, sys)

    def predict(self, dataframe: DataFrame):
        """
        Method Name :   predict
        Description :   This method checks whether model is present in the bucket or not

        :param dataframe: Dataframe on which prediction is to be done

        :Output     :   return the prediction in the form of dataframe
        On Failure  :   Write an exception log and then return False

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered predict method of SensorEstimator class")
        try:
            # Load the model if not loaded
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            # Use the predict method of the loaded_model (SensorModel) to predict the dataframe
            return self.loaded_model.predict(dataframe)
        except Exception as e:
            raise SensorException(e, sys)
