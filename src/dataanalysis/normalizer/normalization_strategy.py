from abc import ABC, abstractmethod
from typing import Union, List


class NormalizationStrategy(ABC):
    @abstractmethod
    def normalize(self, score: Union[float, List[float]]) -> Union[float, List[float]]:
        pass


class MinMaxNormalizationStrategy(NormalizationStrategy):
    def __init__(self, min_value: float, max_value: float):
        self.min_value = min_value
        self.max_value = max_value

    def normalize(self, score: Union[float, List[float]]) -> Union[float, List[float]]:
        if isinstance(score, list):
            return [(self._normalize_single(s)) for s in score]
        return self._normalize_single(score)

    def _normalize_single(self, score: float) -> float:
        normalized_score = (score - self.min_value) / (self.max_value - self.min_value) * 100
        # Clamp the value to ensure it stays between 0 and 100
        return max(0, min(100, normalized_score))


# TODO: Implement Z-Score/Scaling Normalization
