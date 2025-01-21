from .Query import Query
from . import QueryConstants
from ..api.RedditApiLatestSubredditData import RedditApiLatestSubredditData

class RedditLatestSubredditDataQuery(Query):
    """
    Query class that handles the collection of the latest reddit data on /{targetSub}.
    """

    @classmethod
    def __init__(self, targetSub: str):
        self.targetSub = targetSub
        self.query = (f"{QueryConstants.REDDIT_LATEST_SUBREDDIT_DATA_URL.substitute(subreddit=self.targetSub)}{QueryConstants.REDDIT_COUNT_AFTER_STRING}")

    @classmethod
    def execute(self) -> list:
        """
        Initiates the relevant API call to collect the latest data from /{targetSub}.
        """
        return RedditApiLatestSubredditData(self.query).callApi()
