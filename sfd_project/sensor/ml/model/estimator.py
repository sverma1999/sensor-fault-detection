import sys

from pandas import DataFrame
from sklearn.pipeline import Pipeline

from sensor.exception_code.exception import SensorException
from sensor.logger_code.logger import logging


# custom class to map the target value to 0 and 1, doing for learning purpose.
# other option is to use LabelEncoder from sklearn.preprocessing
class TargetValueMapping:
    def __init__(self):
        # negative class is mapped to 0 and positive class is mapped to 1
        self.neg: int = 0
        self.pos: int = 1

    # returns the dictionary of class mapping with neg and pos.
    def to_dict(self):
        return self.__dict__

    # returns the dictionary of class mapping with 0 and 1 to neg and pos respectively.
    def reverse_mapping(self):
        mapping_response = self.to_dict()

        return dict(zip(mapping_response.values(), mapping_response.keys()))
