import pymongo
from sensor.constant.database import DATABASE_NAME
from sensor.constant.env_variables import MONGODB_URL_KEY
from sensor.exception_code.exception import SensorException
from sensor.logger_code.logger import logging
import certifi
import os
import sys


ca = certifi.where()


class MongoDBClient:
    """
    This class is responsible for creating a connection to MongoDB.
    """

    client = None

    # Recieve the database name as a parameter and create a connection to the database of MongoDB
    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            # make the connection to MongoDB only if the client is none and not already connected
            if MongoDBClient.client is None:
                # URL is loading from .env file.
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                # print(mongo_db_url)

                # If the URL is not set, raise an exception
                if mongo_db_url is None:
                    raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set.")

                # tlsCAFile is used to verify the certificate of the server
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

                # if "localhost" in mongo_db_url:
                #     MongoDBClient.client = pymongo.MongoClient(mongo_db_url)
                # else:
                #     MongoDBClient.client = pymongo.MongoClient(
                #         mongo_db_url, tlsCAFile=ca)
            self.client = MongoDBClient.client

            logging.info(f"Connected to MongoDB: {self.client}")

            self.database = self.client[database_name]
            logging.info(f"Connected to database: {self.database}")
            self.database_name = database_name
        except Exception as e:
            raise SensorException(e, sys)
