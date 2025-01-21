"""Transformation module"""
from abc import ABC, abstractmethod
from typing import List, Dict

class Transformation(ABC):
    """
    This abstract class serves to define the Transformation models.
    """
    @abstractmethod
    def apply(self, data: List[Dict]) -> List[Dict]:
        """
        Abstract method to apply a transformation to the data.
        
        :param data: data to apply the transformation on.
        """
