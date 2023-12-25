import pymongo
import os
from dotenv import load_dotenv

import certifi

load_dotenv()  # Load environment variables from .env file

ca = certifi.where()


class MongodbOperation:
    def __init__(self) -> None:
        # Create a MongoClient to the running mongod instance
        self.client = pymongo.MongoClient(os.getenv("MONGO_DB_URL"), tlsCAFile=ca)
        self.db_name = "sensor_readings"

    # Wait for some records to be inserted, the insert records in bulk.
    def insert_many(self, collection_name, records: list):
        self.client[self.db_name][collection_name].insert_many(records)

    # Insert a single record
    def insert(self, collection_name, record):
        self.client[self.db_name][collection_name].insert_one(record)
