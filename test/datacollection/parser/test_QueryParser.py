import unittest
from unittest.mock import patch

from src.datacollection.parser.QueryParser import QueryParser

class test_QueryParser(unittest.TestCase):
    """
    Unit Tests for the QueryParser class.
    """
    @patch('src.datacollection.parser.QueryParser.RedditParser')
    def test_init_callsRedditParser(self, MockRedditParser):
        """
        Test that RedditParser is called once with the queryType and args when the data source is 'reddit'.
        """
        QueryParser.parseQuery("reddit", "globalLatest")
        MockRedditParser.parse.assert_called_once_with("globalLatest")

        MockRedditParser.reset_mock()
        QueryParser.parseQuery("reddit", "subredditLatest", "subreddit")
        MockRedditParser.parse.assert_called_once_with("subredditLatest", "subreddit")

    def test_query_invalidDataSource(self):
        """
        Test that a ValueError is raised when an invalid data source is specified.
        """
        self.assertRaises(ValueError, QueryParser.parseQuery, "invalid", "latest")