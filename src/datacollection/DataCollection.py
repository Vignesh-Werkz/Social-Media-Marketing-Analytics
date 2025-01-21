from abc import ABC, abstractmethod

class DataCollection(ABC):
    """
    Public API of the DataCollection component.

    Implemented as an interface.
    """
    @classmethod
    @abstractmethod
    def getLatestRedditData(self) -> str:
        """
        Queries Reddit for the most recent posts on /new.

        Returns the 1000 most recent posts as a JSON string.
        """
        pass

    @classmethod
    @abstractmethod
    def getLatestSubredditData(self, subreddit: str) -> str:
        """
        Queries Reddit for the most recent posts on /{subreddit}.

        Returns up to the 1000 most recent posts as a JSON string.
        (Exact number of posts depeends on the number of posts exposed by the reddit API, this can range from 500-1000)
        """
        pass