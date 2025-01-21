import unittest
from string import Template
from unittest.mock import patch

from src.datacollection.query.RedditLatestDataQuery import RedditLatestDataQuery

class test_RedditLatestDataQuery(unittest.TestCase):

    def setUp(self):
        self.expectedQueryTemplate = Template("https://oauth.reddit.com/new.json?limit=100&count=$count&after=$after").substitute(count="value1", after="value2")

    def test_init(self):
        """
        Test the initialization of RedditLatestDataQuery.
        """
        query_instance = RedditLatestDataQuery()
        self.assertEqual(query_instance.query.substitute(count="value1", after="value2"), self.expectedQueryTemplate)

    @patch('src.datacollection.query.RedditLatestDataQuery.RedditApiLatestData')
    def test_execute(self, MockRedditApiLatestData):
        """
        Test that RedditApiLatestData is called once with the query Template passed to it
        """
        query_instance = RedditLatestDataQuery()
        query_instance.execute()

        MockRedditApiLatestData.assert_called_once_with(query_instance.query)