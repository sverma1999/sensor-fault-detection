from sensor.constant.s3_bucket import PREDICTION_BUCKET_NAME, TRAINING_BUCKET_NAME
from sensor.constant.trainingPipeline_consts import SAVED_MODEL_DIR

PREDICTION_DATA_BUCKET = PREDICTION_BUCKET_NAME

PREDICTION_INPUT_FILE_NAME = "sensor_pred_input_data.csv"

PREDICTION_OUTPUT_FILE_NAME = "sensor_predictions_output.csv"

MODEL_BUCKET_NAME = TRAINING_BUCKET_NAME


LOCAL_PREDICTION_DATA_BUCKET = "local_prediction_checkup_bucket"

LOCAL_PREDICTION_INPUT_FILE_NAME = "sensor_pred_input_data.csv"

LOCAL_PREDICTION_OUTPUT_FILE_NAME = "sensor_predictions_output.csv"

LOCAL_MODEL_BUCKET_NAME = SAVED_MODEL_DIR
