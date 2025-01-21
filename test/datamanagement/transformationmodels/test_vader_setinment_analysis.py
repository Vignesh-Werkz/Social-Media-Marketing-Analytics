"""Module for Test Vader Sentiment Analysis"""
import unittest
from src.datamanagement.transformationmodels import VaderSentimentAnalysis


class TestVaderSentimentAnalysis(unittest.TestCase):
    """
    Test class for VaderSentimentAnalysis Unit Testing.
    """
    # pylint: disable=abstract-class-instantiated, unused-variable, too-few-public-methods

    def setUp(self):
        """
        Method to define test variables.
        """
        self.test_data = [
            {
                "selftext": "I love programming in Python.",
                "title": "Python is great!",
                "comments": ["Amazing language.", "So powerful!"],
                "transformed_data": {
                    "selftext": "i love programming in python.",
                    "title": "python is great",
                    "comments": ["amazing language.", "so powerful"],
                    "selftext_tokens": ["i", "love", "programming", "python"],
                    "title_tokens": ["python", "great"],
                    "comments_tokens": [["amazing", "language"], ["so", "powerful"]]
                }
            }
        ]
        self.empty_data = []
        self.analysis = VaderSentimentAnalysis()

    def test_sentiment_analysis(self):
        """
        Method to test sentiment analysis using Vader.
        """
        result = self.analysis.apply(self.test_data)
        for post in result:
            self.assertIn("vader", post["model_output"])
            self.assertIn("selftext_sentiment", post["model_output"]["vader"])
            self.assertIn("title_sentiment", post["model_output"]["vader"])
            self.assertIn("comments_sentiment", post["model_output"]["vader"])

    def test_empty_sentiment_analysis(self):
        """
        Method to test sentiment analysis when no selftext, title, or comments exist.
        """
        result = self.analysis.apply(self.empty_data)
        for post in result:
            self.assertNotIn("vader", post["model_output"])


if __name__ == '__main__':
    unittest.main()
