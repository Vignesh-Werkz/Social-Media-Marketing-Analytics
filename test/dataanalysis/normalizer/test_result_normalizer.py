import unittest
from src.dataanalysis.normalizer import RedditResultNormalizer
from src.dataanalysis.normalizer import VADERNormalizer, TextBlobNormalizer


class TestRedditResultNormalizer(unittest.TestCase):
    def setUp(self):

        self.vader_normalizer = VADERNormalizer()
        self.textblob_normalizer = TextBlobNormalizer()

        self.reddit_normalizer = RedditResultNormalizer(model_normalizers={
            "VADER": self.vader_normalizer,
            "TextBlob": self.textblob_normalizer
        })

    def test_normalize_single_model(self):
        post = {
            "model_output": {
                "VADER": {"title_sentiment": -0.2, "selftext_sentiment": 0.8}
            }
        }
        result = self.reddit_normalizer.normalize(post)
        expected = {
            "model_output": {
                "VADER": {"title_sentiment": 40.0, "selftext_sentiment": 90.0}
            }
        }
        self.assertEqual(result["model_output"], expected["model_output"])

    def test_normalize_post_with_multiple_models(self):

        post = {
            "title": "Example post",
            "selftext": "This is a test selftext.",
            "model_output": {
                "VADER": {
                    "title_sentiment": -0.5,
                    "selftext_sentiment": 0.8
                },
                "TextBlob": {
                    "title_sentiment": 0.4,
                    "selftext_sentiment": -0.3,
                    "comment_sentiment": [0.1, 0.9, -0.5]
                }
            }
        }

        expected = {
            "title": "Example post",
            "selftext": "This is a test selftext.",
            "model_output": {
                "VADER": {
                    "title_sentiment": 25.0,
                    "selftext_sentiment": 90.0
                },
                "TextBlob": {
                    "title_sentiment": 70.0,
                    "selftext_sentiment": 35.0,
                    "comment_sentiment": [55.0, 95.0, 25.0]
                }
            }
        }

        result = self.reddit_normalizer.normalize(post)

        for model_name in expected["model_output"]:
            for key in expected["model_output"][model_name]:
                if isinstance(expected["model_output"][model_name][key], list):
                    # For lists, check each element
                    for i in range(len(expected["model_output"][model_name][key])):
                        self.assertAlmostEqual(result["model_output"][model_name][key][i],
                                               expected["model_output"][model_name][key][i],
                                               places=5)
                else:
                    self.assertAlmostEqual(result["model_output"][model_name][key],
                                           expected["model_output"][model_name][key],
                                           places=5)

    def test_missing_model_output_field(self):
        post = {"title": "Example post without model_output", "selftext": "Test selftext"}

        with self.assertRaises(ValueError):
            self.reddit_normalizer.normalize(post)

    def test_no_normalizer_for_model(self):
        post = {
            "model_output": {
                "VADER": {"title_sentiment": -0.2, "selftext_sentiment": 0.8},
                "UnknownModel": {"title_sentiment": -0.1, "selftext_sentiment": 0.5}
            }
        }
        result = self.reddit_normalizer.normalize(post)
        expected = {
            "model_output": {
                "VADER": {"title_sentiment": 40.0, "selftext_sentiment": 90.0},
                "UnknownModel": {"title_sentiment": -0.1, "selftext_sentiment": 0.5}
            }
        }
        self.assertEqual(result["model_output"], expected["model_output"])