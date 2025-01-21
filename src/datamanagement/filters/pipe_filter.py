"""Module for Pipe Filter."""
from abc import ABC, abstractmethod
from typing import List, Dict


class Pipe:
    """
    A class to manage the flow of data in the preprocessing pipeline.
    """

    def __init__(self):
        self.data = None

    def set_data(self, data: List[Dict]):
        """
        Method to set data provided into the pipe.
        :param data: the raw data given to store into the pipe for preprocessing.
        """

        self.data = data

    def get_data(self) -> List[Dict]:
        """
        Method to get data stored in the pipe.
        :return data: the data that is stored in the pipe.
        """
        return self.data


class Filter(ABC):
    """
    Abstract class for data filters to be used in the preprocessing pipeline.
    """
    @abstractmethod
    def execute(self, pipe: Pipe) -> None:
        """
        Method to execute said filter to process the data stored in the pipe.
        """
