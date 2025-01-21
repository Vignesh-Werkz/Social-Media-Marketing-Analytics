import json

class ResultParser:
    """
    Parses query results and returns the relevant data in a JSON format.
    """

    @classmethod
    def parseRedditData(self, dataList: list) -> str:
        """
        Parses the list of Reddit data and removes irrelevant fields from each item in the list,
        returns the list as a valid JSON in string format.
        """
        if type(dataList) is not list:
            raise TypeError("Invalid data type. Expected list, got " + str(type(dataList)))
        else:
            return self._extractFields(self, dataList)

    def _extractFields(self, dataList: list) -> str:
        """
        Extracts the relevant fields from the raw data.
        """
        resultList = ["["]
        for i in range(len(dataList)):
            post = dataList[i]
            result = {}
            result["source"] = "Reddit"
            result["post_id"] = post["data"]["id"]
            result["subreddit"] = post["data"]["subreddit"]
            result["selftext"] = post["data"]["selftext"]
            result["title"] = post["data"]["title"]
            result["ups"] = post["data"]["ups"]
            result["upvote_ratio"] = post["data"]["upvote_ratio"]
            result["created_utc"] = post["data"]["created_utc"]
            result["comments"] = self._extractComments(post["comments"])
            resultList.append(json.dumps(result, indent=4))
            if i < len(dataList) - 1:
                resultList.append(",")
        resultList.append("]")
        return ''.join(resultList)

    def _extractComments(commentsList: str) -> list:
        """
        Extracts the comments from the raw data.
        """
        comments = []
        for comment in commentsList:
            comments.append(comment["data"]["body"])
        return comments