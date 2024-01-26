import sys, os

# from neuro_mf import ModelFactory

from sensor.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
)
from sensor.entity.config_entity import ModelTrainerConfig
from sensor.exception_code.exception import SensorException
from sensor.logger_code.logger import logging

from sensor.ml.metric import calculate_metric
from sensor.ml.model.estimator import SensorModel
from sensor.utils.main_utils import (
    load_numpy_array_data,
    load_object,
    save_object,
    read_yaml_file,
)

# For method 2: Using ModelFactory from neuro_mf package==============================
from neuro_mf import (
    ModelFactory,
)  # Model Factory helps us to generate model training and grid search code automatically

# If method 1 is used, then uncomment the below line
from xgboost import XGBClassifier
from sensor.constant.trainingPipeline_consts import PARAMS_FILE_PATH


class ModelTrainer:
    def __init__(
        self,
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_config: ModelTrainerConfig,
    ):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

        self._params_config = read_yaml_file(PARAMS_FILE_PATH)

    # method 1, to train model using XGBClassifier directly if hyperparameter tuning is already done in jupyter notebook and not required to be done in the code.
    def train_model(self, x_train, y_train):
        logging.info("Entered train_model method of ModelTrainer class")
        try:
            logging.info(
                f"Training model using XGBClassifier with params: {self._params_config}"
            )
            # logging.info(f"Learning rate type: {type(self._params_config)}")
            # logging.info(f"XGBoost type: {type(self._params_config['XGBoost'])}")
            # logging.info(f"XGBoost: {self._params_config['XGBoost']}")
            # logging.info(
            #     f"Learning Rate: {self._params_config['XGBoost']['learning_rate']}"
            # )
            # logging.info(
            #     f"n_estimators: {self._params_config['XGBoost']['n_estimators']}"
            # )
            # logging.info(f"max_depth: {self._params_config['XGBoost']['max_depth']}")
            xgb_clf = XGBClassifier(
                learning_rate=self._params_config["XGBoost"]["learning_rate"],
                n_estimators=self._params_config["XGBoost"]["n_estimators"],
                max_depth=self._params_config["XGBoost"]["max_depth"],
            )
            logging.info("XGBClassifier object created!")
            xgb_clf.fit(x_train, y_train)
            return xgb_clf
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_trainer(
        self,
    ) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")
        try:
            # Load numpy array data of training data
            train_arr = load_numpy_array_data(
                file_path=self.data_transformation_artifact.transformed_train_file_path
            )

            # Load numpy array data of testing data
            test_arr = load_numpy_array_data(
                file_path=self.data_transformation_artifact.transformed_test_file_path
            )

            # Split train and test data into x_train, y_train, x_test, y_test
            x_train, y_train, x_test, y_test = (
                train_arr[
                    :, :-1
                ],  # pull everything except the last column from train_arr
                train_arr[:, -1],  # pull only the last column from train_arr
                test_arr[
                    :, :-1
                ],  # pull everything except the last column from test_arr
                test_arr[:, -1],  # pull only the last column from test_arr
            )

            # Train model method 1: Using custom features and Assuming hyperparameter tunning was already done in jupyter notebook during EDA==============================

            # train the model using the train_model method
            model = self.train_model(x_train, y_train)

            logging.info("Model trained!")

            # predict for training set and find the classification metric
            classification_train_metric = calculate_metric(
                model=model, x=x_train, y=y_train
            )

            logging.info("Classification metric calculated for train data!")
            # Here we check if the trained model accuracy is greater than the expected accuracy. If yes, then we don't need to retrain the model.

            if (
                classification_train_metric.f1_score
                <= self.model_trainer_config.expected_accuracy
            ):
                logging.info("Trained model is not better than expected accuracy!")
                raise Exception("Trained model is not better than expected accuracy!")

            # predict for testing set and find the classification metric
            classification_test_metric = calculate_metric(
                model=model, x=x_test, y=y_test
            )

            logging.info("Classification metric calculated for test data!")

            # Check overfitting and underfitting
            # For over fitting: check differece between F1 score of train and test data
            # Reminder: F1 score is the harmonic mean of precision and recall
            difference = abs(
                classification_train_metric.f1_score
                - classification_test_metric.f1_score
            )

            # threashold is 5%. This threshold chosen to be 0.05 because we are being less strict here. We could have chosen 0.02 as well.
            if (
                difference
                > self.model_trainer_config.overfitting_underfitting_threshold
            ):
                logging.info("Overfitting detected!, Mode need to be retrained")
                raise Exception("Overfitting detected!")

            # load pre-processing object from the transformation artifact
            preprocessing_obj = load_object(
                file_path=self.data_transformation_artifact.transformed_object_file_path
            )

            sensor_model = SensorModel(
                preprocessing_object=preprocessing_obj, trained_model_object=model
            )

            logging.info("Created SensorModel object with preprocessor and model")

            # create the directory to save the trained model
            model_dir_path = os.path.dirname(
                self.model_trainer_config.trained_model_file_path
            )
            os.makedirs(model_dir_path, exist_ok=True)

            # Saving the model to the trained_model_file_path specified in the config
            save_object(
                self.model_trainer_config.trained_model_file_path, obj=sensor_model
            )
            logging.info("Saved best model to the trained_model_file_path.")

            # model trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric,
                model_params=self._params_config,
            )
            logging.info("Metric artifact created.")

            # End of method 1:=================================================================================================

            # # Train model method 2: Using ModelFactory from neuro_mf package==============================
            # # Find the best model using grid search
            # model_factory = ModelFactory(
            #     model_config_path=self.model_trainer_config.model_config_file_path
            # )
            # logging.info("ModelFactory object created!")

            # # This function first performs hyperparameter tuning using grid search and creates a list of grid search models.
            # # Later, checks if any model from the list is better than the expected accuracy, and then return that model.
            # best_model_details = model_factory.get_best_model(
            #     X=x_train,
            #     y=y_train,
            #     base_accuracy=self.model_trainer_config.expected_accuracy,
            # )
            # logging.info("Best model found!")

            # # check if best_model acuracy is less than expected accuracy (this step could be ignored since we are already checking this in the get_best_model function).
            # if (
            #     best_model_details.best_score
            #     < self.model_trainer_config.expected_accuracy
            # ):
            #     logging.info("No model with better than expected accuracy found!")
            #     raise Exception("No model with better than expected accuracy found!")

            # # load pre-processing object from the transformation artifact
            # preprocessing_obj = load_object(
            #     file_path=self.data_transformation_artifact.transformed_object_file_path
            # )

            # # Now we have the best model, we can train it on the entire training data set
            # sensor_model = SensorModel(
            #     preprocessing_object=preprocessing_obj,
            #     trained_model_object=best_model_details.best_model,
            # )

            # logging.info("Created SensorModel object with preprocessor and model")

            # # Saving the model to the trained_model_file_path specified in the config
            # save_object(
            #     file_path=self.model_trainer_config.trained_model_file_path,
            #     obj=sensor_model,
            # )

            # logging.info("Saved best model to the trained_model_file_path.")

            # test_metric_artifact = calculate_metric(
            #     model=best_model_details.best_model, x=x_test, y=y_test
            # )

            # # Return the model trainer artifact
            # model_trainer_artifact = ModelTrainerArtifact(
            #     trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            #     metric_artifact=test_metric_artifact,
            # )

            # End of method 2:========================================

            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            raise SensorException(e, sys) from e
