"""Data Visualisation Module"""
import os

from typing import List
from custom_types import IndicatorData
from .dataclient import DataClientManager, DataClientConfig

class DataVisualisationAPI:
    """
    This class exposes the reults of the Data Analysis Module to the FastAPI for
    consumption by the React frontend.
    """

    def __init__(self):
        models_db_config = DataClientConfig(
            db_type="mongodb",
            uri=os.getenv("MONGODB_URI"),
            db_name=os.getenv("DATABASE_NAME"),
            collection="models"
        )
        self.models_client = DataClientManager.get_database_client(models_db_config)

        aggregates_db_config = DataClientConfig(
            db_type="mongodb",
            uri=os.getenv("MONGODB_URI"),
            db_name=os.getenv("DATABASE_NAME"),
            collection="aggregates"
        )
        self.aggregates_client = DataClientManager.get_database_client(aggregates_db_config)

        indicator_db_config = DataClientConfig(
            db_type="mongodb",
            uri=os.getenv("MONGODB_URI"),
            db_name=os.getenv("DATABASE_NAME"),
            collection="indicators"
        )
        self.indicator_client = DataClientManager.get_database_client(indicator_db_config)

    def get_models_list(self) -> List[str]:
        """
        Retrieves all models currently supported by the app
        """

        raw_data = self.models_client.load_data()
        model_names = [model['model_name'] for model in raw_data]
        return model_names

    def get_models(self):
        """
        Gets the description of the model
        """

        raw_data = self.models_client.load_data()
        return raw_data

    def get_aggregates(self):
        """
        Retrieves all aggregates from db
        """

        raw_data = self.aggregates_client.load_data()
        return raw_data

    def upsert_aggregate(self, updated_aggregate):
        """
        Updates/inserts new aggregate data to db
        """

        self.aggregates_client.upsert_data(
            data=[updated_aggregate],
            key_field='aggregateName'
        )

    def delete_aggregate(self, aggregate_name: str):
        """
        Deletes aggregate based on the aggregate name
        """
        self.aggregates_client.delete_data(aggregate_name, key_field= 'aggregateName')

    def get_indicators(self):
        """
        Retrieves all indicators from db
        """

        raw_data = self.indicator_client.load_data()
        return raw_data

    def upsert_indicator(self, indicator_data: IndicatorData):
        """
        Updates/inserts new indicator data to db
        """

        self.indicator_client.upsert_data(
            data=[indicator_data],
            key_field='indicatorName'
        )

    def delete_indicator(self, indicator_name: str):
        """
        Deletes indicator based on the indicator name
        """
        self.indicator_client.delete_data(indicator_name, key_field='indicatorName')
