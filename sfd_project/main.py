# from sensor.configuration.mongo_db_connection import MongoDBClient

from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig

from sensor.pipeline.training_pipeline import TrainingPipeline
from sensor.logger_code.logger import logging
from sensor.exception_code.exception import SensorException
import sys

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


def test_exception():
    try:
        logging.info("We are diving 1 by zero")
        x = 1 / 0
    except Exception as e:
        raise SensorException(e, sys)  # e is the error message, sys is the error detail


def test_fun():
    logging.info("Entered the test_fun method of main.py")


if __name__ == "__main__":
    # ------------------------------------------- Training pipeline starts here -------------------------------------------
    # try:
    training_pipeline = TrainingPipeline()

    training_pipeline.run_pipeline()
    # except Exception as e:
    #     logging.exception(e)
    # ------------------------------------------- Rough -------------------------------------------

    # mongodb_client = MongoDBClient()
    # print("Collection name: ", mongodb_client.database.list_collection_names())

    # training_pipeline_config = TrainingPipelineConfig()
    # data_ingetion_config = DataIngestionConfig(
    #     training_pipeline_config=training_pipeline_config
    # )
    # it return the dictionary of variable name and value of the class
    # print(data_ingetion_config.__dict__)

    # try:
    #     test_exception()
    # except Exception as e:
    #     # logging.exception(e)
    #     print(e)

    # test_fun()
