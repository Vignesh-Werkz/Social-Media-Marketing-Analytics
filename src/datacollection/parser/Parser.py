from abc import ABC, abstractmethod

from ..query.Query import Query

class Parser(ABC):
    """
    Abstract representation of a Parser that is able to parse the query input.
    """
    @classmethod
    @abstractmethod
    def parse(self, queryType: str, *args: str) -> Query:
        """
        Parses the input query and returns the appropriate Query object.
        """
        pass