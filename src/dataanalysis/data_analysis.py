from datetime import datetime
import os
from typing import List, Optional, Dict

from .date_range import DateRange
from .dataclient import DataClientManager, DataClientConfig
from .normalizer.result_normalizer import RedditResultNormalizer
from .normalizer import VADERNormalizer, TextBlobNormalizer
from .aggregator import WeightedAggregator, OverallAggregator


class DataAnalysis:
    def __init__(self):
        """Initializes the DataAnalysis class with necessary components."""
        self.debug = True  # Enable debug logging
        self.data_aggregator = self.initialize_components()

    def load_data_from_db(self, collection_name: str, filters: dict = None) -> List[Dict]:
        """
        Loads data from the specified MongoDB collection.

        :param collection_name: str, the name of the MongoDB collection.
        :param filters: dict, optional filters for querying the collection.

        :return: list of dictionaries, each representing a document in the collection.
        """
        db_config = DataClientConfig(
            db_type="mongodb",
            uri=os.getenv("MONGODB_URI"),
            db_name=os.getenv("DATABASE_NAME"),
            collection=collection_name
        )
        db_handler = DataClientManager.get_database_client(db_config)
        return db_handler.load_data(filters=filters)

    def save_result_to_db(self, indicator_name: str, new_results: Dict[str, List[Dict]], delete: bool = False) -> None:
        """
        Updates MongoDB with new daily or monthly results, with an option to delete existing entries.

        :param indicator_name: str, the name of the indicator.
        :param new_results: dict, containing lists of daily and monthly results to save.
        :param delete: bool, if True, clears resultsByDay and resultsByMonth fields in the database.

        :return: None
        """
        try:
            # Prepare the configuration for storing results
            target_db_config = DataClientConfig(
                db_type="mongodb",
                uri=os.getenv("MONGODB_URI"),
                db_name=os.getenv("DATABASE_NAME"),
                collection="indicators"
            )
            result_handler = DataClientManager.get_database_client(target_db_config)

            # Fetch the existing document
            existing_data = result_handler.load_data(filters={"indicatorName": indicator_name})[0]

            if delete:
                self.debug and print(f"save_result_to_db(): Emptying '{indicator_name}' results.")
                # Clear the fields by setting them to empty lists
                existing_data["resultsByDay"] = []
                existing_data["resultsByMonth"] = []
                # Ensure MongoDB receives the empty lists by using `$set`
                result_handler.upsert_data(data=[{"indicatorName": indicator_name, "resultsByDay": [], "resultsByMonth": []}], key_field='indicatorName')
            else:
                # Append only available results to existing data
                if "resultsByDay" in new_results and new_results["resultsByDay"]:
                    existing_data.setdefault("resultsByDay", []).extend(new_results["resultsByDay"])

                if "resultsByMonth" in new_results and new_results["resultsByMonth"]:
                    existing_data.setdefault("resultsByMonth", []).extend(new_results["resultsByMonth"])

                # Upsert the updated result into the database
                result_handler.upsert_data(data=[existing_data], key_field='indicatorName')

            self.debug and print(f"save_result_to_db(): Updated results for indicator '{indicator_name}' successfully.")

        except Exception as e:
            self.debug and print(f"save_result_to_db(): Error saving result to MongoDB: {e}")
            raise

    def initialize_components(self):
        """
        Initializes and returns the aggregator and normalizers for data processing.

        :return: OverallAggregator, a configured aggregator for sentiment analysis.
        """
        model_normalizers = {
            "vader": VADERNormalizer(), "textblob": TextBlobNormalizer()}
        reddit_normalizer = RedditResultNormalizer(model_normalizers)
        weighted_aggregator = WeightedAggregator()

        source_db_config = DataClientConfig(
            db_type="mongodb",
            uri=os.getenv("MONGODB_URI"),
            db_name=os.getenv("DATABASE_NAME"),
            collection="reddit_posts_transformed"
        )
        db_handler = DataClientManager.get_database_client(source_db_config)
        return OverallAggregator(db_handler, reddit_normalizer, weighted_aggregator)

    def build_filters(self, aggregate_name, indicator_names):
        """
        Builds a filter dictionary based on provided names for aggregates or indicators.

        :param aggregate_name: str, aggregate name to filter.
        :param indicator_name: str, single indicator name to filter.
        :param indicator_names: list of str, multiple indicator names to filter.

        :return: dict, filter criteria for querying the database.
        """
        if indicator_names:
            return {"indicatorName": {"$in": indicator_names}}
        elif aggregate_name:
            return {"aggregateName": aggregate_name}
        return {}

    def load_aggregate_weights(self, aggregate_name: str):
        """
        Loads weights for data aggregation based on the aggregate name.

        :param aggregate_name: str, the name of the aggregate.

        :return: tuple, containing a dictionary of weights and a list of model keys.
        """
        aggregate = self.load_data_from_db(
            "aggregates", {"aggregateName": aggregate_name})[0]
        aggregate_weights = {'model_weights': {}}
        model_keys = []

        for weight in aggregate['weights']:
            model_name = weight["model_name"]
            aggregate_weights[model_name] = {
                'title_sentiment': weight['title_sentiment'],
                'selftext_sentiment': weight['selftext_sentiment'],
                'comments_sentiment': weight['comments_sentiment'],
            }
            aggregate_weights['model_weights'][model_name] = weight['model_weight']
            model_keys.append(model_name)

        return aggregate_weights, model_keys

    def compute_daily_results(self, indicator, model_keys, weights, filters, latest_day):
        """
        Computes daily results for the indicator if they are missing or outdated.

        :param indicator: dict, the indicator document.
        :param model_keys: list of str, the model keys to use for aggregation.
        :param weights: dict, weights for each model and its components.
        :param filters: list, filters applied to data.
        :param latest_day: str, the latest computed date for daily results.

        :return: list of dicts, each containing daily aggregated sentiment scores.
        """
        today_str = datetime.now().strftime("%Y-%m-%d")
        # returns default past 30 days if indicator does not have the field
        if "resultsByDay" not in indicator or indicator.get("resultsByDay") == []:
            return self.data_aggregator.aggregate_data_by_date(
                model_keys=model_keys, weights=weights, filters=filters, date_range=DateRange.ONE_MONTH
            )
        # else returns new daily result
        elif latest_day != today_str:
            daily_result = self.data_aggregator.aggregate_data_by_date(
                model_keys=model_keys, weights=weights, filters=filters, date_range=DateRange.ONE_DAY
            )
            return [{"date": today_str, "average_score": daily_result[0].get("average_score")}]
        return []

    def compute_monthly_results(self, indicator, model_keys, weights, filters, latest_month):
        """
        Computes monthly results for the indicator if they are missing or outdated.

        :param indicator: dict, the indicator document.
        :param model_keys: list of str, the model keys to use for aggregation.
        :param weights: dict, weights for each model and its components.
        :param filters: list, filters applied to data.
        :param latest_month: str, the latest computed date for monthly results.

        :return: list of dicts, each containing monthly aggregated sentiment scores.
        """
        current_month_str = datetime.now().strftime("%Y-%m")
        # returns default past 6 months if indicator does not have the field
        if "resultsByMonth" not in indicator or indicator.get("resultsByMonth") == []:
            return self.data_aggregator.aggregate_data_by_date(
                model_keys=model_keys, weights=weights, filters=filters, date_range=DateRange.SIX_MONTHS
            )
        # else returns new monthly result
        elif datetime.now().day != 1 and latest_month != current_month_str:
            monthly_result = self.data_aggregator.aggregate_data_by_date(
                model_keys=model_keys, weights=weights, filters=filters, date_range=DateRange.ONE_MONTH
            )
            return [{"date": current_month_str, "average_score": monthly_result[-1].get("average_score")}]
        return []

    def get_latest_date(self, indicator: Dict, results_field: str) -> Optional[str]:
        """
        Retrieves the latest date from a specified field in the indicator document.

        :param indicator: dict, the indicator document.
        :param results_field: str, the field name (e.g., "resultsByDay" or "resultsByMonth").
        :return: str or None, the latest date in the specified field, or None if the field is empty.
        """
        # Get the list of entries in results_field and ensure it's not empty
        entries = indicator.get(results_field, [])
        if not entries:
            return None

        # Find the maximum date in the entries
        latest_date = max(entry["date"] for entry in entries if "date" in entry)
        return latest_date

    def process_update(self, indicator: Dict, update_type: str):
        """
        Processes daily, monthly, or all updates for a single indicator, managing data limits.

        :param indicator: dict, the indicator document to process.
        :param update_type: str, either 'daily', 'monthly', or 'all'.
        """
        try:
            indicator_name = indicator.get('indicatorName')
            filters = indicator.get('filters', [])
            aggregate_name = indicator.get('aggregateName')
            aggregate_weights, model_keys = self.load_aggregate_weights(aggregate_name)

            # Determine max entries and compute method based on update_type
            if update_type == 'all':
                # Clear results if update_type is "all"
                indicator["resultsByDay"] = []
                indicator["resultsByMonth"] = []
                self.save_result_to_db(indicator_name, {"resultsByDay": [], "resultsByMonth": []}, delete=True)

                # Recompute for the last 30 days and 6 months
                daily_results = self.data_aggregator.aggregate_data_by_date(
                    model_keys=model_keys, weights=aggregate_weights, filters=filters, date_range=DateRange.ONE_MONTH
                )
                monthly_results = self.data_aggregator.aggregate_data_by_date(
                    model_keys=model_keys, weights=aggregate_weights, filters=filters, date_range=DateRange.SIX_MONTHS
                )

                # Trim and save new results
                indicator["resultsByDay"] = self.trim_results(daily_results, 30)
                indicator["resultsByMonth"] = self.trim_results(monthly_results, 6)
                self.save_result_to_db(indicator_name, {"resultsByDay": indicator["resultsByDay"], "resultsByMonth": indicator["resultsByMonth"]})

            else:
                # Determine specific fields for daily or monthly update
                results_field = "resultsByDay" if update_type == 'daily' else "resultsByMonth"
                max_entries = 30 if update_type == 'daily' else 6
                latest_date_str = self.get_latest_date(indicator, results_field)

                # Compute new results for either daily or monthly
                new_results = self.compute_daily_results(indicator, model_keys, aggregate_weights, filters, latest_date_str) if update_type == 'daily' \
                    else self.compute_monthly_results(indicator, model_keys, aggregate_weights, filters, latest_date_str)

                # Update indicator with new results if applicable
                if new_results:
                    indicator[results_field] = self.trim_results(indicator.get(results_field, []) + new_results, max_entries)
                    self.save_result_to_db(indicator_name, {results_field: indicator[results_field]})

        except Exception as e:
            self.debug and print(f"Error processing {update_type} update for indicator '{indicator.get('indicatorName')}': {e}")
    
    def trim_results(self, results, max_entries):
        """Trims results to the latest `max_entries` entries."""
        return sorted(results, key=lambda x: x['date'])[-max_entries:]

    def execute(self, update_type: str,
                aggregate_name: Optional[str] = None,
                indicator_names: Optional[List[str]] = None):
        """
        Executes daily or monthly updates for indicators.

        :param update_type: str, either 'daily' or 'monthly'.
        :param indicator_names: Optional list of indicator names to filter.
        """
        filters = self.build_filters(
            aggregate_name=aggregate_name, indicator_names=indicator_names)
        indicators = self.load_data_from_db("indicators", filters)
        
        for indicator in indicators:
            try:
                self.process_update(indicator, update_type)
            except Exception as e:
                self.debug and print(f"Error processing {update_type} update for indicator '{indicator.get('indicatorName')}': {e}")
