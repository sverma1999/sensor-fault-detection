import os
import pickle
import sys
from io import StringIO

# typing is used to define the type of the variables, functions, etc.
# Union is used to return multiple types from a function or variable
from typing import List, Union

# ClientError from boto3 is used to handle the exception raised by boto3
from botocore.exceptions import ClientError

# Bucket from mypy_boto3_s3 is used to get the bucket object
from mypy_boto3_s3.service_resource import Bucket
from pandas import DataFrame, read_csv
from sensor.configuration.aws_connection import S3Client
from sensor.exception_code.exception import SensorException
from sensor.logger_code.logger import logging


class SimpleStorageService:
    def __init__(self):
        # creating the connection to the AWS S3
        s3_client = S3Client()

        # getting the bucket object
        self.s3_resource = s3_client.s3_resource

        # getting the client object
        self.s3_client = s3_client.s3_client

    # one of the helper methods in this class --------
    # @staticmethod
    def get_bucket(self, bucket_name: str) -> Bucket:
        """
        Method Name :   get_bucket
        Description :   This method gets the bucket object based on the bucket_name

        Output      :   Bucket object is returned based on the bucket name
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered the get_bucket method of SimpleStorageService class")

        try:
            # using the boto3 resource to get the bucket object
            bucket = self.s3_resource.Bucket(bucket_name)

            logging.info("Exited the get_bucket method of SimpleStorageService class")

            return bucket

        except Exception as e:
            raise SensorException(e, sys) from e

    # one of the main methods in this class ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def s3_key_path_available(self, bucket_name, s3_key):
        try:
            # getting the bucket object
            bucket = self.get_bucket(bucket_name=bucket_name)

            # there could be multiple objects, so filter the objects based on the s3_key and check if the length of the list is greater than 0
            # if the length of the list is greater than 0, then it means that the s3_key is present in the bucket
            file_objects = [
                file_object for file_object in bucket.objects.filter(Prefix=s3_key)
            ]
            if len(file_objects) > 0:
                return True
            else:
                return False
        except Exception as e:
            raise SensorException(e, sys)

    # one of the helper methods in this class ----------
    def read_object(
        self, object_name: str, decode: bool = True, make_readable: bool = False
    ) -> Union[StringIO, str]:
        """
        Method Name :   read_object
        Description :   This method reads the object

        Output      :   Returns object content either in string or StringIO format
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered the read_object method of SimpleStorageService class")

        try:
            # Debugging: Print the type and content of object_name
            logging.info(
                f"object_name type: {type(object_name)}, content: {object_name}"
            )

            # Lambda function to return the
            func = (
                lambda: object_name.get()["Body"].read().decode()
                if decode is True
                else object_name.get()["Body"].read()
            )
            # if looking for a readable object, then convert the object to StringIO, it is mutable and file-like interface.
            # otherwise return the object as it is in string format, which is immutable
            conv_func = lambda: StringIO(func()) if make_readable is True else func()

            logging.info("Exited the read_object method of SimpleStorageService class")

            return conv_func()

        except Exception as e:
            logging.info("This is possible, where the error is raised")
            logging.exception(e)
            raise SensorException(e, sys) from e

    # one of the helper methods in this class ----------
    # Return either a list of objects or a single object
    def get_file_object(
        self, filename: str, bucket_name: str
    ) -> Union[List[object], object]:
        """
        Method Name :   get_file_object
        Description :   This method gets the file object from bucket_name bucket based on filename

        Output      :   list of objects or object is returned based on filename
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered the get_file_object method of SimpleStorageService class")

        try:
            # getting the bucket object
            bucket = self.get_bucket(bucket_name)

            # Debugging: bucket name incorrect
            logging.info(f"Bucket name is: {bucket_name}")
            logging.info(f"Type of bucket is: {type(bucket)}, and bucket is: {bucket}")
            logging.info(
                f"Type of filename is: {type(filename)}, and filename is: {filename}"
            )
            logging.info(f"Objects of bucket are: {bucket.objects}")

            # getting the file object from the bucket
            # Note, the bucket object is a list of objects, we can filter the list based on the filename.
            file_objects = [
                file_object for file_object in bucket.objects.filter(Prefix=filename)
            ]

            # Debugging: currently showing empty list
            logging.info(
                f"Type of file_objects is: {type(file_objects)}, and file_objects is: {file_objects}"
            )

            # if the lenght of the file_objects is 1, then return the first object from the list
            # else return the list of objects
            func = lambda x: x[0] if len(x) == 1 else x

            # Debugging: length showing 0
            logging.info(f"Length of file_objects is: {len(file_objects)}")

            file_objs = func(file_objects)

            logging.info(
                f"Type of file_objs is: {type(file_objs)}, and file_objs is: {file_objs}"
            )
            logging.info(
                "Exited the get_file_object method of SimpleStorageService class"
            )

            # return file object at 0, if the length of the file_objects is 1, else return the list of file_objects
            return file_objs

        except Exception as e:
            raise SensorException(e, sys) from e

    # one of the main methods in this class ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def load_model(
        self, model_name: str, bucket_name: str, model_dir: str = None
    ) -> object:
        """
        Method Name :   load_model
        Description :   This method loads the model_name model from bucket_name bucket with kwargs

        Output      :   a model object is returned based on filename
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered the load_model method of SimpleStorageService class")

        try:
            # lambda function to return the path to model object name.
            # model_dir is the directory where the model is present in the bucket
            # if model_dir is None, then keep the path to be set as model_name.
            func = (
                lambda: model_name
                if model_dir is None
                else model_dir + "/" + model_name
            )

            model_file = func()

            # get the model object from the bucket
            file_object = self.get_file_object(model_file, bucket_name)

            logging.info(f"Type of file_object is: {type(file_object)}")
            # read the model object
            model_obj = self.read_object(file_object, decode=False)

            logging.info(
                f"Until here it is fine, type of model_obj is: {type(model_obj)}"
            )

            # load the model object using pickle library
            model = pickle.loads(model_obj)

            return model

        except Exception as e:
            raise SensorException(e, sys) from e

    # one of the main methods in this class ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def create_folder(self, folder_name: str, bucket_name: str) -> None:
        """
        Method Name :   create_folder
        Description :   This method creates a folder_name folder in bucket_name bucket

        Output      :   None, a folder is created in s3 bucket if it is not present already
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered the create_folder method of SimpleStorageService class")

        try:
            # check if the folder_name folder is present in the bucket_name bucket
            # if present, then load the folder object.
            self.s3_resource.Object(bucket_name, folder_name).load()

        # ClientError is raised if the folder_name folder is not present in the bucket_name bucket
        except ClientError as e:
            # if the error code is 404, then create the folder_name folder in the bucket_name bucket
            if e.response["Error"]["Code"] == "404":
                folder_obj = folder_name + "/"

                # here is the boto3 client is used to create the folder_name folder in the bucket_name bucket
                # key is the folder_name folder
                self.s3_client.put_object(Bucket=bucket_name, Key=folder_obj)

            else:
                pass

            logging.info(
                "Exited the create_folder method of SimpleStorageService class"
            )

    # one of the helper methods in this class ----------
    def upload_file(
        self,
        from_filename: str,
        to_filename: str,
        bucket_name: str,
        remove: bool = True,
    ):
        """
        Method Name :   upload_file
        Description :   This method uploads the from_filename file to bucket_name bucket with to_filename as bucket filename

        Output      :   None, only make use of boto3 resource to upload the file to the bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered the upload_file method of SimpleStorageService class")

        try:
            logging.info(
                f"Uploading {from_filename} file to {to_filename} file in {bucket_name} bucket"
            )

            # use the boto3 resource to upload the file to the bucket
            self.s3_resource.meta.client.upload_file(
                from_filename, bucket_name, to_filename
            )

            logging.info(
                f"Uploaded {from_filename} file to {to_filename} file in {bucket_name} bucket"
            )

            # Check if the remove is True, if True then delete the source file, else keep the source file
            if remove is True:
                os.remove(from_filename)

                logging.info(f"Remove is set to {remove}, deleted the file")

            else:
                logging.info(f"Remove is set to {remove}, not deleted the file")

            logging.info("Exited the upload_file method of SimpleStorageService class")

        except Exception as e:
            raise SensorException(e, sys) from e

    # one of the main methods in this class ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def upload_df_as_csv(
        self,
        data_frame: DataFrame,
        local_filename: str,
        bucket_filename: str,
        bucket_name: str,
    ) -> None:
        """
        Method Name :   upload_df_as_csv
        Description :   This method uploads the dataframe to bucket_filename csv file in bucket_name bucket

        Output      :   None, only the file is uploaded to the bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info(
            "Entered the upload_df_as_csv method of SimpleStorageService class"
        )

        try:
            # convert the dataframe to csv file named local_filename.
            data_frame.to_csv(local_filename, index=None, header=True)

            # upload the local_filename csv file to bucket_filename in bucket_name bucket
            self.upload_file(local_filename, bucket_filename, bucket_name)

            logging.info(
                "Exited the upload_df_as_csv method of SimpleStorageService class"
            )

        except Exception as e:
            raise SensorException(e, sys) from e

    # one of the helper methods in this class -----------
    def get_df_from_object(self, object_: object) -> DataFrame:
        """
        Method Name :   get_df_from_object
        Description :   This method gets the dataframe from the object_name object

        Output      :   Dataframe is returned
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info(
            "Entered the get_df_from_object method of SimpleStorageService class"
        )

        try:
            # read the object, which will return the content either in string or StringIO format.
            content = self.read_object(object_, make_readable=True)

            # pandas read_csv method is used to convert the csv file object to dataframe
            df = read_csv(content, na_values="na")
            logging.info(
                "Exited the get_df_from_object method of SimpleStorageService class"
            )

            return df

        except Exception as e:
            raise SensorException(e, sys) from e

    # one of the main methods in this class ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def read_csv(self, filename: str, bucket_name: str) -> DataFrame:
        """
        Method Name :   read_csv
        Description :   This method gets the csv file from the s3 bucket and returns the dataframe

        Output      :   Dataframe is returned
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered the read_csv method of SimpleStorageService class")

        try:
            # fetch the csv file object from the s3 bucket
            # this will either return a list of csv_obj or a single csv_obj
            csv_obj = self.get_file_object(filename, bucket_name)

            # convert the csv file object to dataframe
            df = self.get_df_from_object(csv_obj)

            logging.info("Exited the read_csv method of SimpleStorageService class")

            return df

        except Exception as e:
            raise SensorException(e, sys) from e
