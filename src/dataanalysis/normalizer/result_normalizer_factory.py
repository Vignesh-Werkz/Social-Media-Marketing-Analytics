from src.dataanalysis.normalizer import VADERNormalizer, TextBlobNormalizer
from src.dataanalysis.normalizer import ResultNormalizer, RedditResultNormalizer
from typing import List, Dict


class ResultNormalizerFactory:
    """
    A factory class to create instances of ResultNormalizer based on configurations.
    """

    @staticmethod
    def create_normalizer(normalizer_type: str, model_configs: List[Dict]) -> ResultNormalizer:
        """
        Creates and returns an instance of a specific ResultNormalizer based on the normalizer type and model configs.

        :param normalizer_type: The type of normalizer to create (e.g., "reddit").
        :param model_configs: A list of model configurations with model names and their respective strategies.
        :return: An instance of ResultNormalizer (e.g., RedditResultNormalizer).
        """
        if normalizer_type == "reddit":
            model_normalizers = {}
            for model in model_configs:
                if model["name"] == "vader":
                    model_normalizers["vader"] = VADERNormalizer()  # Assume VADERNormalizer class is defined elsewhere
                elif model["name"] == "textblob":
                    model_normalizers["textblob"] = TextBlobNormalizer()  # Assume TextBlobNormalizer class is defined elsewhere
                # Add more model-specific normalizers here as needed

            # Return an instance of RedditResultNormalizer with the model-specific normalizers
            return RedditResultNormalizer(model_normalizers)

        else:
            raise ValueError(f"Unknown normalizer type: {normalizer_type}")
