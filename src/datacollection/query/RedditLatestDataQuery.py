from .Query import Query
from . import QueryConstants
from ..api.RedditApiLatestData import RedditApiLatestData

class RedditLatestDataQuery(Query):
    """
    Query class that handles the collection of the latest reddit data on /new.
    """

    @classmethod
    def __init__(self):
        self.query = QueryConstants.REDDIT_LATEST_DATA_URL

    @classmethod
    def execute(self) -> list:
        """
        Initiates the relevant API call to collect the latest data from /new.
        """
        return RedditApiLatestData(self.query).callApi()
