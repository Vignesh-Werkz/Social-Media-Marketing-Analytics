import unittest
from string import Template
from unittest.mock import patch

from src.datacollection.query.RedditLatestSubredditDataQuery import RedditLatestSubredditDataQuery

class test_RedditLatestSubredditDataQuery(unittest.TestCase):

    def setUp(self):
        self.targetSub = "testsub"
        self.expectedQueryTemplate = Template("https://oauth.reddit.com/r/$subreddit/new.json?limit=100&count=$count&after=$after").substitute(subreddit=self.targetSub, count="value1", after="value2")

    def test_init(self):
        """
        Test the initialization of RedditLatestSubredditDataQuery.
        """
        query_instance = RedditLatestSubredditDataQuery(self.targetSub)
        self.assertEqual(Template(query_instance.query).substitute(count="value1", after="value2"), self.expectedQueryTemplate)

    @patch('src.datacollection.query.RedditLatestSubredditDataQuery.RedditApiLatestSubredditData')
    def test_execute(self, MockRedditApiLatestSubredditData):
        """
        Test that RedditApiLatestSubredditData is called once with the query Template passed to it.
        """
        query_instance = RedditLatestSubredditDataQuery(self.targetSub)
        query_instance.execute()

        MockRedditApiLatestSubredditData.assert_called_once_with(query_instance.query)
