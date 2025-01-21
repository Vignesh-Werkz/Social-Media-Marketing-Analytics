from collections import defaultdict
from datetime import datetime, timedelta
from typing import List, Dict

from ..date_range import DateRange
from ..normalizer import ResultNormalizer
from .weighted_aggregator import WeightedAggregator


class OverallAggregator:
    def __init__(self, db_handler, result_normalizer: ResultNormalizer, weighted_aggregator: WeightedAggregator):
        """
        Initializes the OverallAggregator with necessary components.

        :param db_handler: handler to fetch data from a data source.
        :param result_normalizer: ResultNormalizer instance (e.g. RedditResultsNormalizer) that normalizes
         sentiment data for each post.
        :param weighted_aggregator: WeightedAggregator instance to combine the model averages into a final score.
        """
        self.db_handler = db_handler
        self.result_normalizer = result_normalizer
        self.weighted_aggregator = weighted_aggregator
        self.debug = True  # enable debug logging

    def aggregate_data(self,
                       model_keys: List[str],
                       weights: Dict[str, Dict[str, float]],
                       filters=None) -> float:
        """
        Fetches data using the db_handler, aggregates sentiment data across multiple posts, and returns the overall
        average score.
        :param model_keys: List of model keys (e.g., "vader", "textblob") to be processed.
        :param weights: Dictionary of weights for each model's components and overall model weights.
        :param filters: Optional dictionary of filters (e.g., keywords) for fetching data.
        :return: The overall average sentiment score across all posts.
        """
        # Fetch data from the database using the db_handler
        data = self.db_handler.load_data(filters=filters)

        # Calculate the overall average score for the fetched data
        return self.calculate_overall_average_score(data, model_keys, weights)

    def aggregate_data_by_date(
            self,
            model_keys: List[str],
            weights: Dict[str, Dict[str, float]],
            filters=None,
            date_range: DateRange = DateRange.ONE_DAY
    ) -> List[Dict[str, float]]:
        # Determine start and end dates
        end_date = datetime.now()
        start_date = end_date - timedelta(days=date_range.value)
        date_format = '%Y-%m-%d' if date_range == DateRange.ONE_DAY or date_range == DateRange.ONE_MONTH else '%Y-%m'

        # Initialize date_aggregated_scores with all expected dates in range
        date_aggregated_scores = self.initialize_expected_dates(
            start_date, end_date, date_format)

        # Fetch data from the database
        filters = [keyword.lower() for keyword in filters]
        query = {"keywords": {"$all": filters}}
        data = self.db_handler.load_data(filters=query)

        # Process each post and aggregate scores for each date
        for post in data:
            post_date = datetime.fromtimestamp(post['created_utc'])
            if start_date <= post_date <= end_date:
                formatted_date = post_date.strftime(date_format)
                aggregated_score = self.process_post(post, model_keys, weights)
                date_aggregated_scores[formatted_date].append(aggregated_score)

        # Calculate the average score for each date, using 0.0 if there were no scores
        average_scores_by_date = [
            {
                "date": date,
                "average_score": sum(scores) / len(scores) if scores else 0.0
            }
            for date, scores in date_aggregated_scores.items()
        ]

        return average_scores_by_date

    def initialize_expected_dates(self, start_date, end_date, date_format):
        """Generate a dictionary of dates with an empty list for each expected date in the range."""
        expected_dates = defaultdict(list)
        current_date = start_date
        while current_date <= end_date:
            date_key = current_date.strftime(date_format)
            expected_dates[date_key] = []
            if date_format == '%Y-%m-%d':
                current_date += timedelta(days=1)
            elif date_format == '%Y-%m':
                current_date += timedelta(days=30)  # approximately one month
        return expected_dates

    def process_post(self, post: Dict, model_keys: List[str], weights: Dict[str, Dict[str, float]]) -> float:
        """
        Processes a single post, normalizing its sentiment scores and aggregating them.

        :param post: A dictionary representing a single post with sentiment data from multiple models.
        :param model_keys: List of model keys (e.g., "vader", "textblob") to be processed.
        :param weights: Dictionary of weights for each model's components (title, selftext, comments),
                        and overall weights for each model in the aggregation step.
        :return: The aggregated sentiment score for the post.
        """

        # Normalize the entire post using the ResultNormalizer
        normalized_post = self.result_normalizer.normalize(post)

        # Send the normalized post to the WeightedAggregator
        aggregated_score = self.weighted_aggregator.aggregate(
            normalized_post, model_keys, weights)

        return aggregated_score

    def calculate_overall_average_score(self, data: Dict, model_keys: List[str],
                                        weights: Dict[str, Dict[str, float]]) -> float:
        """
        Calculates the overall average sentiment score across multiple posts.

        :param data: A list of dictionaries, where each dictionary represents a post with sentiment data.
        :param model_keys: List of model keys (e.g., "vader", "textblob") to be processed.
        :param weights: Dictionary of weights for each model's components and overall model weights.
        :return: The overall average sentiment score across all posts.
        """
        total_aggregated_score = 0.0
        post_count = 0

        # Process each post and aggregate the scores
        for post in data:
            aggregated_post_result = self.process_post(
                post, model_keys, weights)
            total_aggregated_score += aggregated_post_result
            post_count += 1

        # Calculate the overall average score
        if post_count > 0:
            overall_average_score = total_aggregated_score / post_count
        else:
            overall_average_score = 0.0

        return overall_average_score
