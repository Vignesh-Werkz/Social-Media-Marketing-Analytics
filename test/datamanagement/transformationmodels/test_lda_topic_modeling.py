"""Module for Test LDA Topic Modeling"""
import unittest
from src.datamanagement.transformationmodels import LDATopicModeling


class TestLDATopicModeling(unittest.TestCase):
    """
    Test class for LDATopicModeling Unit Testing.
    """

    def setUp(self):
        """
        Method to define test variables.
        """
        self.test_data = [
            {
                "subreddit": "python",
                "selftext": "Python is an amazing programming language.",
                "title": "Why I love Python",
                "comments": ["Python is great.", "I love using it for data science."],
                "transformed_data": {
                    "selftext_tokens": ["python", "amazing", "programming", "language"],
                    "title_tokens": ["love", "python"],
                    "comments_tokens": [["python", "great"], ["love", "using", "data", "science"]]
                }
            }
        ]
        self.empty_data = [
            {
                "subreddit": "python",
                "selftext": "",
                "title": "",
                "comments": [],
                "transformed_data": {
                    "selftext_tokens": [],
                    "title_tokens": [],
                    "comments_tokens": []
                }
            }
        ]
        self.lda_modeling = LDATopicModeling(num_topics=2, passes=2, top_n_keywords=3)

    def test_lda_topic_modeling(self):
        """
        Method to test LDA topic modeling on valid input data.
        """
        result = self.lda_modeling.apply(self.test_data)
        for post in result:
            self.assertIn("keywords", post)
            self.assertGreater(len(post["keywords"]), 0)  # Ensure keywords are generated
            self.assertIn("python", post["keywords"])  # Ensure subreddit is in keywords

    def test_empty_lda_topic_modeling(self):
        """
        Method to test LDA topic modeling when no valid tokens exist.
        """
        result = self.lda_modeling.apply(self.empty_data)
        for post in result:
            self.assertIn("keywords", post)
            self.assertEqual(len(post["keywords"]), 0)  # Ensure no keywords are generated


if __name__ == '__main__':
    unittest.main()
