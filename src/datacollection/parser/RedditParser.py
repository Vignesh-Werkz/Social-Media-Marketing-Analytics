from .Parser import Parser
from ..query import QueryConstants
from ..query.Query import Query
from ..query.RedditLatestDataQuery import RedditLatestDataQuery
from ..query.RedditLatestSubredditDataQuery import RedditLatestSubredditDataQuery

class RedditParser(Parser):
    """
    Handles parsing of all Reddit queries
    """
    @classmethod
    def parse(self, queryType: str, *args: str) -> Query:
        match queryType:
            case QueryConstants.QUERY_TYPE_GLOBAL_LATEST:
                return RedditLatestDataQuery()
            case QueryConstants.QUERY_TYPE_SUBREDDIT_LATEST:
                self._verifyArgsLatestSubredditData(*args)
                return RedditLatestSubredditDataQuery(args[0])
            case _:
                raise ValueError("Invalid Query Type detected during Reddit Query Parsing")
            
    def _verifyArgsLatestSubredditData(*args: str) -> None:
        """
        Verifies that the args provided for the latest subreddit-specific data query are valid.
        """
        if (len (args) != 1):
            raise ValueError("Invalid number of arguments detected during Reddit Query Parsing")
        if (not isinstance(args[0], str)):
            raise ValueError("Invalid argument type detected during Reddit Query Parsing")