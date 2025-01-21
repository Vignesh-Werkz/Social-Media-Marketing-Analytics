import unittest

from src.datacollection.parser.RedditParser import RedditParser

class test_RedditParser(unittest.TestCase):
    """
    Unit Tests for the RedditParser class.
    """
    def test_parse_returnsGlobalLatest(self):
        """
        Test that the RedditLatestDataQuery is returned when the queryType is 'globalLatest'.
        """
        query = RedditParser.parse("globalLatest")
        self.assertEqual(query.__class__.__name__, "RedditLatestDataQuery")
    
    def test_parse_returnsSubredditLatest(self):
        """
        Test that the RedditLatestSubredditDataQuery is returned when the queryType is 'subredditLatest'.
        Also tests _verifyArgsLatestSubredditData with a positive test case.
        """
        query = RedditParser.parse("subredditLatest", "subreddit")
        self.assertEqual(query.__class__.__name__, "RedditLatestSubredditDataQuery")

    def test_parse_invalidQueryType(self):
        """
        Test that a ValueError is raised when an invalid queryType is specified.
        """
        self.assertRaises(ValueError, RedditParser.parse, "invalid")

    def test_verifyArgsLatestSubredditData_invalidArgs(self):
        """
        Test that a ValueError is raised when the number of args provided for the subredditLatest query is invalid.
        """
        self.assertRaises(ValueError, RedditParser._verifyArgsLatestSubredditData, "subreddit", "invalid")