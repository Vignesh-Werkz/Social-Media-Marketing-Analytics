"""Module for Test Tokenization Filter."""
import unittest
from src.datamanagement.filters import Pipe, TokenizationFilter


class TestTokenizationFilter(unittest.TestCase):
    """
    Test class for Tokenization Filter Unit Testing.
    """
    # pylint: disable=abstract-class-instantiated, unused-variable, too-few-public-methods

    def setUp(self):
        """
        Set up method to define test variables.
        """
        self.pipe = Pipe()
        self.test_data = [
            {
                "selftext": "This is a TEST!",
                "title": "Test TITLE",
                "comments": ["Great Post!"],
                "transformed_data": {
                    "selftext": "this test",
                    "title": "test title",
                    "comments": ["great post"]
                }
            }
        ]
        self.empty_data = [
            {
                "selftext": "",
                "title": "",
                "comments": [""]
            }
        ]
        self.filter = TokenizationFilter()

    def test_valid_text(self):
        """
        Method to test tokenization on valid data.
        """
        self.pipe.set_data(self.test_data)
        self.filter.execute(self.pipe)
        tokenized_data = self.pipe.get_data()
        for post in tokenized_data:
            self.assertIsInstance(
                post["transformed_data"]["selftext_tokens"], list)
            self.assertEqual(post["transformed_data"]
                             ["selftext_tokens"], ["this", "test"])
            self.assertEqual(post["transformed_data"]
                             ["title_tokens"], ["test", "title"])
            self.assertEqual(post["transformed_data"]
                             ["comments_tokens"], [["great", "post"]])

    def test_empty_text(self):
        """
        Method to test tokenization on empty data.
        """
        self.pipe.set_data(self.empty_data)
        self.filter.execute(self.pipe)
        tokenized_data = self.pipe.get_data()
        for result in tokenized_data:
            self.assertEqual(
                result['transformed_data'], {})


if __name__ == '__main__':
    unittest.main()
