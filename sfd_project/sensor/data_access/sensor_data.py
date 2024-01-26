import sys
from typing import Optional

import numpy as np
import pandas as pd
import json
from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.constant.database import DATABASE_NAME
from sensor.exception_code.exception import SensorException
from sensor.logger_code.logger import logging


# this class can be used by any component, exporting from any database or collection.
class SensorData:
    """
    This class help to export entire mongo db record as pandas dataframe
    """

    def __init__(self):
        """ """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)

        except Exception as e:
            raise SensorException(e, sys)

    def save_csv_file(
        self, file_path, collection_name: str, database_name: Optional[str] = None
    ):
        try:
            data_frame = pd.read_csv(file_path)
            data_frame.reset_index(drop=True, inplace=True)
            records = list(json.loads(data_frame.T.to_json()).values())
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
            collection.insert_many(records)
            return len(records)
        except Exception as e:
            raise SensorException(e, sys)

    # Load the collection from MongoDB and convert it into a dataframe
    def export_collection_as_dataframe(
        self, collection_name: str, database_name: Optional[str] = None
    ) -> pd.DataFrame:
        try:
            """
            export entire collection as dataframe:
            return DataFrame of collection
            """
            if database_name is None:
                logging.info("Database name is not provided, using default database")
                collection = self.mongo_client.database[collection_name]
                # logging.info(f"collection name is: {collection}")
            else:
                logging.info("Using provided database name")
                collection = self.mongo_client[database_name][collection_name]
            logging.info(f"collection name is: {collection}")
            logging.info(f"list(collection.find()): {collection.find()}")
            df = pd.DataFrame(list(collection.find()))

            logging.info("Exported collection as dataframe")

            # drop the _id column from the dataframe, as it is not required
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            # replace the "na" string with np.nan, so that it can be imputed later
            df.replace({"na": np.nan}, inplace=True)

            return df

        except Exception as e:
            raise SensorException(e, sys)
