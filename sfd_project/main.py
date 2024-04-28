# from sensor.configuration.mongo_db_connection import MongoDBClient

from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig

from sensor.pipeline.training_pipeline import TrainingPipeline
from sensor.pipeline.prediction_pipeline import PredictionPipeline
from sensor.ml.model.estimator import TargetValueMapping
from sensor.constant.trainingPipeline_consts import *

from sensor.logger_code.logger import logging
from sensor.exception_code.exception import SensorException
import sys
from dotenv import load_dotenv
from sensor.constant.application import APP_HOST, APP_PORT
from sensor.utils.main_utils import load_object

from fastapi import FastAPI, File, UploadFile, Request
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from sensor.constant.env_variables import MONGODB_URL_KEY
import pandas as pd

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# def test_exception():
#     try:
#         logging.info("We are diving 1 by zero")
#         x = 1 / 0
#     except Exception as e:
#         raise SensorException(e, sys)  # e is the error message, sys is the error detail


# def test_fun():
#     logging.info("Entered the test_fun method of main.py")


# index route and authentication tags are used for swagger documentation
@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs/")


@app.get("/train")
async def train_route():
    try:
        # Load environment variables from .env file
        # load_dotenv()

        # Create a training pipeline object
        training_pipeline = TrainingPipeline()

        if training_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running!!")
        # Run the training pipeline from local data storage
        training_pipeline.run_pipeline()
        return Response("Training pipeline executed successfully!!")

    except Exception as e:
        logging.exception(e)
        return Response(f"Error occurred while executing training pipeline: {e}")


@app.get("/predict")
async def predict_route():
    try:
        # Create a prediction pipeline object
        prediction_pipeline = PredictionPipeline()

        # Run the prediction pipeline on cloud
        prediction_pipeline.run_pipeline()

        return Response(
            "Prediction successful and predictions are stored in s3 bucket !!"
        )

        # # For local testing purpose
        # prediction_pipeline.run_pipeline_locally()

        # return Response(
        #     "Prediction successful and predictions are stored in local_prediction_checkup_bucket folder!"
        # )

    except Exception as e:
        # logging.exception(e)
        raise Response(f"Error occurred while executing prediction pipeline: {e}")


def main():
    # ------------------------------------------- Training pipeline starts here -------------------------------------------
    try:
        # Load environment variables from .env file
        # load_dotenv()

        # Create a training pipeline object
        training_pipeline = TrainingPipeline()
        # Run the training pipeline
        training_pipeline.run_pipeline()

    except Exception as e:
        print(e)
        logging.exception(e)

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


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    app_run(app, host=APP_HOST, port=APP_PORT)
    # main()
