from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from sensor.pipeline.training_pipeline import TrainingPipeline
from sensor.logger import logging
from sensor.exception import SensorException
import sys

# def test_exception():
#     try:
#         logging.info("We are diving 1 by zero")
#         x=1/0
#     except Exception as e:
#         raise SensorException(e, sys)


if __name__ == '__main__':

    # mongodb_client = MongoDBClient()
    # print("Collection name: ", mongodb_client.database.list_collection_names())

    # training_pipeline_config = TrainingPipelineConfig()
    # data_ingetion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    # print(data_ingetion_config.__dict__)

    # try:
    #     test_exception()
    # except Exception as e:
    #     # logging.exception(e)
    #     print(e)

    training_pipeline = TrainingPipeline()
    training_pipeline.run_pipeline()

    
    
