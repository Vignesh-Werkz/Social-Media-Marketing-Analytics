from ..query import QueryConstants
from ..query.Query import Query
from .RedditParser import RedditParser

class QueryParser:
    """
    Handles Query Parsing for the Data Collection Component.
    """

    @classmethod
    def parseQuery(self, dataSource: str, queryType: str, *args: str) -> Query:
        """
        Parses the input query string and returns the results of the parsing performed by the relevant Parser object.
        """
        match dataSource:
            case QueryConstants.DATA_SOURCE_REDDIT:
                return RedditParser.parse(queryType, *args)
            case _:
                raise ValueError("Invalid Data Source Specified")