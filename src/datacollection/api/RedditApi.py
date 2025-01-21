import requests
import time
from abc import abstractmethod

from .Api import Api
from . import ApiConstants
from ..query import QueryConstants

class RedditApi(Api):
    """
    Abstract class containing the template method for Reddit API calls.
    """

    @classmethod
    def callApi(self) -> list:
        """
        Delegates the work to the Template Method
        """
        return self.callRedditApiTemplate()
    
    @classmethod
    def callRedditApiTemplate(self) -> list:
        """
        Template method for all Reddit API calls.
        """
        authKey = self._getAuthKey()
        authHeader = {"Authorization": f"bearer {authKey}"}
        resultList = self._makeApiCall(self, authHeader)
        return self._retrieveComments(self, resultList, authHeader)

    def _getAuthKey() -> str:
        auth = requests.auth.HTTPBasicAuth(ApiConstants.REDDIT_APP_ID, ApiConstants.REDDIT_SECRET_KEY)
        data = ApiConstants.data

        authenticationCounter = 0
        while authenticationCounter < ApiConstants.MAXIMUM_AUTHENTICATION_ATTEMPTS:
            authenticationResponse = requests.post(ApiConstants.AUTH_URL, auth=auth, data=data)
            authenticationResponseCode = authenticationResponse.status_code
            if authenticationResponseCode == ApiConstants.REQUEST_SUCCESS_CODE:
                return authenticationResponse.json()["access_token"]
            elif authenticationResponseCode == ApiConstants.REQUEST_EXCEEDED_CODE:
                authenticationCounter += 1
                print("'Too many requests' error encountered during authentication. Reattempting in 15s...")
                time.sleep(15)
            else:
                authenticationCounter += 1
                print("Unknown Request Error encountered during authentication: " + str(authenticationResponseCode)
                    + ". Reattempting in 15s...")
                time.sleep(15)
        else:
            raise ValueError("Maximum number of authentication attempts (" + str(ApiConstants.MAXIMUM_AUTHENTICATION_ATTEMPTS)
                + ") reached. Please try again later.")

    @abstractmethod
    def _makeApiCall(authHeader: str) -> list:
        pass

    def _retrieveComments(self, postList: list, authHeader: str) -> list:
        for i in range(len(postList)):
            post = postList[i]
            post["comments"] = self._getCommentsFromPost(authHeader, post["data"]["id"], post["data"]["subreddit"])
        return postList
    
    def _getCommentsFromPost(authHeader:str, postId: str, postSubreddit: str) -> list:
        query = QueryConstants.REDDIT_GET_COMMENTS_URL.substitute(subreddit=postSubreddit, postId=postId)
        commentRetrievalCounter = 0
        while commentRetrievalCounter < ApiConstants.MAXIMUM_COMMENT_RETRIEVAL_ATTEMPTS:
            commentRetrievalResponse = requests.get(query, headers=authHeader)
            commentResponseCode = commentRetrievalResponse.status_code
            if commentResponseCode == ApiConstants.REQUEST_SUCCESS_CODE:
                # The response is a json array (python list) consisting of 2 objects: the post and the comments.
                # We are only interested in the comments.
                commentsList = commentRetrievalResponse.json()[1]["data"]["children"]
                return commentsList
            elif commentResponseCode == ApiConstants.REQUEST_EXCEEDED_CODE:
                commentRetrievalCounter += 1
                print("'Too many requests' error encountered during comment retrieval for post " + postId + ". Reattempting in 15s...")
                time.sleep(15)
            else:
                commentRetrievalCounter += 1
                print("Unknown Request Error encountered during comment retrieval for post" + postId + ": " + str(commentResponseCode)
                    + ". Reattempting in 15s...")
                time.sleep(15)
        else:
            print("Maximum number of comment retrieval attempts (" + str(ApiConstants.MAXIMUM_COMMENT_RETRIEVAL_ATTEMPTS)
                + ") reached. Please try again later.")
            return []