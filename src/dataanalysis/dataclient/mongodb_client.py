
"""Module for MongoDBClient."""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from .data_client import DataClient
from .data_client_config import DataClientConfig


class MongoDBClient(DataClient):
    """
    This class handles the connection to MongoDB client, as well as CRUD operations
    relating to this connection.
    """

    def __init__(self, db_config: DataClientConfig):
        """
        Init method that defines the target collection, mongo client, and database.

        :param db_config: DataClientConfig that contains connection details.
        """

        self.collection = db_config.collection
        self.client = MongoClient(db_config.uri)
        self.db = self.client[db_config.db_name]
        self.debug = False # enable debug log

        # Ping the MongoDB server to test the connection
        self.ping_server()

    def ping_server(self):
        """
        Helper method that pings to the MongoDB server for connection test.
        """

        try:
            # Ping the server to test the connection
            self.client.admin.command('ping')
            self.debug and print("ping(): Successfully connected to MongoDB server")
        except ConnectionFailure:
            self.debug and print("ping(): Failed to connect to MongoDB server")
            raise  # Re-raise the exception to handle it outside

    def load_data(self, filters:dict):
        """
        Method that loads specified collection from the connection source.

        :return: Collection of data from the MongoDB source.
        """

        try:
            if self.collection in self.db.list_collection_names():
                self.debug and print(f"load_data(): Collection '{self.collection}' exists.")
            else:
                self.debug and print(f"load_data(): Collection '{self.collection}' does not exist.")

            collection = self.db[self.collection]

            query = {}

            query = filters if filters else {}
            self.debug and print(f"load_data(): filters used: {query}")

            # Fetch and return the data from the collection using the query
            data = list(collection.find(query))

            self.debug and print(f"load_data(): data: {data}")
            return data

        except (ConnectionFailure, PyMongoError) as e:
            self.debug and print(f"load_data(): Error loading data from MongoDB: {e}")
            raise

    def close(self):
        """
        Method to close connection to current Mongo Client.
        """
        self.client.close()

    def upsert_data(self, data, key_field: str = '_id'):
        """
        Method that stores the data into the specified collection based on the connection source.

        :param data: Data to store into MongoDB source.
        :param key_field: key id specified for MongoDB.
        :return: Collection of data from the MongoDB source.
        """

        try:
            if self.collection in self.db.list_collection_names():
                self.debug and print(f"upsert_data(): Collection '{self.collection}' exists.")
            else:
                self.debug and print(f"upsert_data(): Collection '{self.collection}' does not exist. New collection will be created.")

            collection = self.db[self.collection]
            for document in data:
                collection.update_one(
                    {key_field: document[key_field]},
                    {'$set': document},
                    upsert=True
                )

        except (ConnectionFailure, PyMongoError) as e:
            self.debug and print(f"upsert_data(): Error inserting data into MongoDB: {e}")
            raise
