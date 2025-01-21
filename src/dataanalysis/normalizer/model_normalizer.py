from abc import ABC, abstractmethod
from typing import List, Dict, Union
from .normalization_strategy import MinMaxNormalizationStrategy


class ModelNormalizer(ABC):
    @abstractmethod
    def normalize(self, data: Dict[str, Union[float, List[float]]]) -> Dict[str, Union[float, List[float]]]:
        """
        Normalize the sentiment scores produced by a specific model.

        :param data: A dictionary containing the sentiment scores to be normalized.
        :return: A dictionary with normalized sentiment scores.
        """
        pass


class VADERNormalizer(ModelNormalizer):
    def __init__(self):
        # Initialize with MinMaxNormalizationStrategy specific to VADER (e.g., range [-1, 1])
        self.strategy = MinMaxNormalizationStrategy(min_value=-1, max_value=1)

    def normalize(self, data: Dict[str, Union[float, List[float]]]) -> Dict[str, Union[float, List[float]]]:
        """
        Normalize VADER sentiment scores using MinMaxNormalizationStrategy.

        :param data: A dictionary containing VADER sentiment scores.
        :return: A dictionary with normalized VADER sentiment scores.
        """
        normalized_data = {}
        for key, value in data.items():
            normalized_data[key] = self.strategy.normalize(value)
        return normalized_data


class TextBlobNormalizer(ModelNormalizer):
    def __init__(self):
        # Initialize with MinMaxNormalizationStrategy specific to TextBlob (e.g., range [-1, 1])
        self.strategy = MinMaxNormalizationStrategy(min_value=-1, max_value=1)

    def normalize(self, data: Dict[str, Union[float, List[float]]]) -> Dict[str, Union[float, List[float]]]:
        """
        Normalize VADER sentiment scores using MinMaxNormalizationStrategy.

        :param data: A dictionary containing VADER sentiment scores.
        :return: A dictionary with normalized VADER sentiment scores.
        """
        normalized_data = {}
        for key, value in data.items():
            normalized_data[key] = self.strategy.normalize(value)
        return normalized_data
