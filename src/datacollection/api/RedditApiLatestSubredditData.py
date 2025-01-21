import requests
from string import Template
import time

from . import ApiConstants
from .RedditApi import RedditApi

class RedditApiLatestSubredditData(RedditApi):
    """
    Handles calling the Reddit API for the latest posts on the specified subreddit.
    """

    @classmethod
    def __init__(self, query: str):
        self.query = Template(query)

    def _makeApiCall(self, authHeader: str) -> list:
        count = 0
        after = ""
        compiledResults = []
        while ((after != None) and (count < ApiConstants.REDDIT_LATEST_SUBREDDIT_DATA_CAP)):
            query = self.query.substitute(count=str(count), after=after)
            try:
                queryData = self._getPageData(query, authHeader)
            except Exception as e:
                print(e)
                return compiledResults
            after = queryData['data']['after']
            count += queryData['data']['dist']
            compiledResults.extend(queryData['data']['children'])
            time.sleep(1)
        return compiledResults
        
    def _getPageData(query: str, authHeader: str) -> dict:
        queryCounter = 0
        while queryCounter < ApiConstants.MAXIMUM_QUERY_ATTEMPTS:
            queryResponse = requests.get(query, headers=authHeader)
            queryResponseCode = queryResponse.status_code
            if queryResponseCode == ApiConstants.REQUEST_SUCCESS_CODE:
                return queryResponse.json()
            elif queryResponseCode == ApiConstants.REQUEST_EXCEEDED_CODE:
                queryCounter += 1
                print("'Too many requests' error encountered during query. Reattempting in 15s...")
                time.sleep(15)
            else:
                queryCounter += 1
                print("Unknown Request Error encountered during query: " + str(queryResponseCode)
                    + ". Reattempting in 15s...")
                time.sleep(15)
        else:
            raise Exception("Maximum number of query attempts (" + str(ApiConstants.MAXIMUM_QUERY_ATTEMPTS)
                + ") reached. Please try again later.")