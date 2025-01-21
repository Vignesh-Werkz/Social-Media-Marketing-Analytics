"""Module for DataClientManager."""
from .data_client_config import DataClientConfig
from .mongodb_client import MongoDBClient


class DataClientManager:
    """
    This class manages the various types of database clients and retrieves the Client connection
    based on the type specified.
    """

    @staticmethod
    def get_database_client(db_config: DataClientConfig):
        """
        Factory method to get the correct database client.

        :param db_config: DataClientConfig containing the db_type
        :return: The specified database client to open a connection with.
        """

        try:
            if db_config.db_type == 'mongodb':
                return MongoDBClient(db_config)
            else:
                raise ValueError(f"Unsupported database type: {db_config.db_type}")

        except ValueError as e:
            print(f"Error creating database client: {e}")
            raise
