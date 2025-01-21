import unittest
from unittest.mock import MagicMock
from src.dataanalysis.aggregator.overall_aggregator import OverallAggregator


class TestOverallAggregator(unittest.TestCase):

    def setUp(self):
        self.mock_db_handler = MagicMock()
        self.mock_result_normalizer = MagicMock()
        self.mock_weighted_aggregator = MagicMock()

        self.aggregator = OverallAggregator(
            db_handler=self.mock_db_handler,
            result_normalizer=self.mock_result_normalizer,
            weighted_aggregator=self.mock_weighted_aggregator
        )

    def test_aggregate_data_by_date(self):
        self.mock_db_handler.load_data.return_value = [
            {"created_utc": 1700000000, "model_output": {"vader": {"title_sentiment": 0.5}}},
            {"created_utc": 1700000500, "model_output": {"vader": {"title_sentiment": 0.8}}}
        ]

        self.mock_result_normalizer.normalize.side_effect = lambda post: post
        self.mock_weighted_aggregator.aggregate.side_effect = lambda post, keys, weights: post["model_output"]["vader"][
            "title_sentiment"]

        model_keys = ["vader"]
        weights = {"vader": {"title": 1.0}}

        average_scores_by_date = self.aggregator.aggregate_data_by_date(model_keys, weights)

        expected_result = {"2023-11": 0.65}
        self.assertEqual(average_scores_by_date, expected_result)

    def test_process_post(self):
        post = {"model_output": {"vader": {"title_sentiment": 0.7}}}

        self.mock_result_normalizer.normalize.return_value = post
        self.mock_weighted_aggregator.aggregate.return_value = 0.7

        model_keys = ["vader"]
        weights = {"vader": {"title": 1.0}}

        aggregated_score = self.aggregator.process_post(post, model_keys, weights)

        self.assertEqual(aggregated_score, 0.7)

    def test_aggregate_data(self):
        self.mock_db_handler.load_data.return_value = [
            {
                "model_output": {
                    "vader": {"title_sentiment": 0.5, "selftext_sentiment": 0.6},
                    "textblob": {"title_sentiment": 0.7}
                }
            },
            {
                "model_output": {
                    "vader": {"title_sentiment": 0.8, "selftext_sentiment": 0.9},
                    "textblob": {"title_sentiment": 0.6}
                }
            }
        ]

        self.mock_result_normalizer.normalize.side_effect = lambda post: post
        self.mock_weighted_aggregator.aggregate.side_effect = lambda post, keys, weights: \
            (post["model_output"]["vader"]["title_sentiment"] + post["model_output"]["vader"]["selftext_sentiment"]) / 2

        model_keys = ["vader", "textblob"]
        weights = {"vader": {"title": 0.5, "selftext": 0.5}, "textblob": {"title": 1.0}}

        overall_score = self.aggregator.aggregate_data(model_keys, weights)

        self.assertAlmostEqual(overall_score, 0.7, places=5)
