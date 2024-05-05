import os.path
import sys

import dill
import numpy as np
import yaml

from sensor.exception_code.exception import SensorException
from sensor.logger_code.logger import logging


def read_yaml_file(file_path: str) -> dict:
    """
    Read yaml file from given path
    Args:
        file_path (str): path of yaml file
    Returns:
        dict: yaml file content in dictionary format
    """
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise SensorException(e, sys) from e


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """Write yaml file to given path
    Args:
        file_path (str): path of yaml file
        content (object): content to write in yaml file
        replace (bool, optional): replace existing file or not. Defaults to False.
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            yaml.dump(content, file)

    except Exception as e:
        raise SensorException(e, sys)


def load_object(file_path: str) -> object:
    logging.info("Entered the load_object method of MainUtils class")

    try:
        with open(file_path, "rb") as file_obj:
            obj = dill.load(file_obj)

        logging.info("Exited the load_object method of MainUtils class")

        return obj

    except Exception as e:
        raise SensorException(e, sys) from e


def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        # first create the file of to path mentioned by file_path, if not exists
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        # save the array to file created above
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)

    except Exception as e:
        raise SensorException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        # load the array from file mentioned by file_path
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)

    except Exception as e:
        raise SensorException(e, sys) from e


def save_object(file_path: str, obj: object) -> None:
    logging.info("Entered the save_object method of MainUtils class")
    # save the object to file example: preprocessing_pipeline.pkl etc..
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

        logging.info("Exited the save_object method of MainUtils class")

    except Exception as e:
        raise SensorException(e, sys) from e
