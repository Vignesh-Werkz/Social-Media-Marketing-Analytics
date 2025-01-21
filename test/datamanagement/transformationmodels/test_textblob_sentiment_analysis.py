"""Module for Test TextBlob Sentiment Analysis"""
import unittest
from src.datamanagement.transformationmodels import TextBlobSentimentAnalysis


class TestTextBlobSentimentAnalysis(unittest.TestCase):
    """
    Test class for TextBlobSentimentAnalysis Unit Testing.
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
        self.empty_data = [{}]
        self.analysis = TextBlobSentimentAnalysis()

    def test_sentiment_analysis(self):
        """
        Method to test sentiment analysis using TextBlob.
        """
        result = self.analysis.apply(self.test_data)
        for post in result:
            self.assertIn("textblob", post["model_output"])
            self.assertIn("selftext_sentiment",
                          post["model_output"]["textblob"])
            self.assertIn("title_sentiment",
                          post["model_output"]["textblob"])
            self.assertIn("comments_sentiment",
                          post["model_output"]["textblob"])

    def test_empty_sentiment_analysis(self):
        """
        Method to test sentiment analysis when no selftext, title, or comments exist.
        """
        result = self.analysis.apply(self.empty_data)
        for post in result:
            self.assertNotIn("selftext_sentiment",
                             post["model_output"]["textblob"])
            self.assertNotIn("title_sentiment",
                             post["model_output"]["textblob"])
            self.assertNotIn("comments_sentiment",
                             post["model_output"]["textblob"])


if __name__ == '__main__':
    unittest.main()
