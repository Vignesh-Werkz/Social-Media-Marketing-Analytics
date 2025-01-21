from abc import ABC, abstractmethod

class Api(ABC):
    """
    Abstract representation of an API object that can be used to collect data from a source.
    """

    @classmethod
    @abstractmethod
    def callApi(self):
        """
        Calls a target API and runs a specific query to collect data.
        """
        pass