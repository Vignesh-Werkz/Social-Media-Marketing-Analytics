import unittest
from src.dataanalysis.aggregator import WeightedAggregator


class TestWeightedAggregator(unittest.TestCase):

    def setUp(self):
        # Initialize WeightedAggregator instance
        self.aggregator = WeightedAggregator()

    def test_aggregate_single_model(self):
        # Mock input data for a single model ('vader') with normalized scores between 0 and 100
        normalized_post = {
            "model_output": {
                "vader": {
                    "title_sentiment": 50.0,  # Normalized score for title sentiment
                    "selftext_sentiment": 70.0,  # Normalized score for selftext sentiment
                    "comments_sentiment": [60.0, 80.0, 70.0]  # List of normalized scores for comments
                }
            }
        }

        model_keys = ["vader"]
        weights = {
            "vader": {
                "title_sentiment": 0.3,
                "selftext_sentiment": 0.2,
                "comments_sentiment": 0.5
            },
            "model_weights": {"vader": 1.0}  # All weight to 'vader'
        }

        # Call the aggregate method
        result = self.aggregator.aggregate(normalized_post, model_keys, weights)

        # Calculate expected result:
        # 50 * 0.3 + 70 * 0.2 + (60 + 80 + 70) / 3 * 0.5 = 15 + 14 + 35 = 64
        self.assertAlmostEqual(result, 64.0, places=5)

    def test_aggregate_multiple_models(self):
        # Mock input data for multiple models ('vader' and 'textblob') with normalized scores between 0 and 100
        normalized_post = {
            "model_output": {
                "vader": {
                    "title_sentiment": 40.0,
                    "selftext_sentiment": 60.0
                },
                "textblob": {
                    "title_sentiment": 70.0,
                    "selftext_sentiment": 50.0
                }
            }
        }

        model_keys = ["vader", "textblob"]
        weights = {
            "vader": {
                "title_sentiment": 0.5,
                "selftext_sentiment": 0.5
            },
            "textblob": {
                "title_sentiment": 0.6,
                "selftext_sentiment": 0.4
            },
            "model_weights": {
                "vader": 0.4,
                "textblob": 0.6
            }
        }
        print("TESTING")
        # Call the aggregate method
        result = self.aggregator.aggregate(normalized_post, model_keys, weights)

        # Calculate expected result for 'vader': 40 * 0.5 + 60 * 0.5 = 50
        # Calculate expected result for 'textblob': 70 * 0.6 + 50 * 0.4 = 62
        # Calculate final result: 50 * 0.4 + 62 * 0.6 = 56.8
        self.assertAlmostEqual(result, 57.2, places=5)

    def test_aggregate_missing_component(self):
        # Mock input data where some components are missing for a model
        normalized_post = {
            "model_output": {
                "vader": {
                    "title_sentiment": 30.0  # Only title sentiment is available
                }
            }
        }

        model_keys = ["vader"]
        weights = {
            "vader": {
                "title_sentiment": 1.0,  # Full weight to title sentiment
                "selftext_sentiment": 0.0,
                "comments_sentiment": 0.0
            },
            "model_weights": {
                "vader": 1.0
            }
        }

        # Call the aggregate method
        result = self.aggregator.aggregate(normalized_post, model_keys, weights)

        # Only 'title_sentiment' should be used with weight of 1.0
        self.assertAlmostEqual(result, 30.0, places=5)


if __name__ == '__main__':
    unittest.main()
