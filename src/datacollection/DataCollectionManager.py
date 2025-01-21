from .DataCollection import DataCollection
from .DCKafkaClient import DCKafkaClient
from .query import QueryConstants
from .parser.QueryParser import QueryParser
from .parser.ResultParser import ResultParser

class DataCollectionManager(DataCollection):
    """
    The main Logic Manager for the DataCollection component.

    Implements the DataCollection interface.
    """

    @classmethod
    def __init__(self):
        self._queryParser = QueryParser()
        self._resultParser = ResultParser()
        self._kafkaClient = DCKafkaClient()
        """
        Default Constructor.
        """

    @classmethod
    def getLatestRedditData(self) -> None:
        """
        Provides the concrete implementation of the getLatestRedditData method.

        Calls on the QueryParser to process the query, then executes the query
        and calls the ResultParser to extract and format the relevant fields.
        """
        query = self._queryParser.parseQuery(QueryConstants.DATA_SOURCE_REDDIT, QueryConstants.QUERY_TYPE_GLOBAL_LATEST)
        resultList = query.execute()
        filteredResults = self._resultParser.parseRedditData(resultList)
        self._kafkaClient.sendToRedditTopic(filteredResults)

    @classmethod
    def getLatestSubredditData(self, subreddit: str) -> None:
        """
        Provides the concrete implementation of the getLatestSubredditData method.

        Calls on the QueryParser to process the query, then executes the query
        and calls the ResultParser to extract and format the relevant fields.
        """
        query = self._queryParser.parseQuery(QueryConstants.DATA_SOURCE_REDDIT, QueryConstants.QUERY_TYPE_SUBREDDIT_LATEST, subreddit)
        resultList = query.execute()
        filteredResults = self._resultParser.parseRedditData(resultList)
        self._kafkaClient.sendToRedditTopic(filteredResults)
