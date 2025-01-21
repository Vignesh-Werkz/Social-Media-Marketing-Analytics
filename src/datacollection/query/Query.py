from abc import ABC, abstractmethod

class Query(ABC):
    """
    Abstract representation a Query object that can be executed.
    """

    @classmethod
    @abstractmethod
    def execute(self):
        """
        Executes the query and returns the result.
        """
        pass