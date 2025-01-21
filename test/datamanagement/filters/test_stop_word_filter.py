"""Module for Test Stopword Filter."""
import unittest
from src.datamanagement.filters import Pipe, StopWordFilter


class TestStopWordFilter(unittest.TestCase):
    """
    Test class for StopWord Filter Unit Testing.
    """
    # pylint: disable=abstract-class-instantiated, unused-variable, too-few-public-methods

    def setUp(self):
        """
        Method to define test variables.
        """
        self.pipe = Pipe()
        self.test_data = [
            {
                "transformed_data": {
                    "selftext_tokens": ["this", "is", "a", "test"],
                    "title_tokens": ["test", "title"],
                    "comments_tokens": [["great", "with", "love"]]
                }
            }
        ]
        self.empty_test_data = [
            {
                "transformed_data": {
                    "selftext_tokens": [],
                    "title_tokens": [],
                    "comments_tokens": [[]]
                }
            }
        ]
        self.filter = StopWordFilter()

    def test_stopword_removal(self):
        """
        Method to test filtering and stopword removal on tokens.
        """
        self.pipe.set_data(self.test_data)
        self.filter.execute(self.pipe)
        filtered_data = self.pipe.get_data()
        for post in filtered_data:
            self.assertNotIn("is", post["transformed_data"]["selftext_tokens"])
            self.assertNotIn("a", post["transformed_data"]["title_tokens"])
            self.assertNotIn(
                "with", post["transformed_data"]["comments_tokens"])

    def test_empty_tokens(self):
        """
        Method to test filtering and stopword removal on empty tokens.
        """
        self.pipe.set_data(self.empty_test_data)
        self.filter.execute(self.pipe)
        filtered_data = self.pipe.get_data()
        for post in filtered_data:
            self.assertEqual(
                post['transformed_data']['selftext_tokens'], [])
            self.assertEqual(
                post['transformed_data']['title_tokens'], [])
            self.assertEqual(
                post['transformed_data']['comments_tokens'], [[]])


if __name__ == '__main__':
    unittest.main()
