from abc import ABC, abstractmethod
from typing import Dict, Union, List
from . import ModelNormalizer



class ResultNormalizer(ABC):
    @abstractmethod
    def normalize(self, data: Dict[str, Union[float, List[float]]]) -> Dict[str, Union[float, List[float]]]:
        """
        Normalize the result data. Must be implemented by subclasses.

        :param data: A dictionary containing the data to be normalized.
        :return: A dictionary with normalized data.
        """
        pass


class RedditResultNormalizer(ResultNormalizer):
    def __init__(self, model_normalizers: Dict[str, ModelNormalizer]):
        """
        Initialize the RedditResultNormalizer with specific model normalizers.

        :param model_normalizers: A dictionary mapping model names to their respective normalization strategies.
        """
        self.model_normalizers = model_normalizers

    def normalize(self, post: Dict) -> Dict:
        """
        Normalize the entire Reddit post by applying model-specific normalizers to the `model_output` field.

        :param post: A dictionary representing the Reddit post, including the `model_output` field.
        :return: A dictionary with the normalized `model_output`.
        """
        if 'model_output' not in post:
            raise ValueError("The post must contain a 'model_output' field.")

        normalized_output = {}
        for model_name, model_data in post['model_output'].items():
            if model_name in self.model_normalizers:
                normalized_output[model_name] = self.model_normalizers[model_name].normalize(model_data)
            else:
                normalized_output[model_name] = model_data  # Leave unchanged if no specific normalizer is defined

        # Return a new post with the normalized `model_output`
        return {
            **post,
            'model_output': normalized_output
        }
