"""Module for MongoDBClient."""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from tqdm import tqdm
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

        # Ping the MongoDB server to test the connection
        self.ping_server()

    def ping_server(self):
        """
        Helper method that pings to the MongoDB server for connection test.
        """

        try:
            # Ping the server to test the connection
            self.client.admin.command('ping')
            print("ping(): Successfully connected to MongoDB server")
        except ConnectionFailure:
            print("ping(): Failed to connect to MongoDB server")
            raise  # Re-raise the exception to handle it outside

    def load_data(self):
        """
        Method that loads specified collection from the connection source.

        :return: Collection of data from the MongoDB source.
        """

        try:
            if self.collection in self.db.list_collection_names():
                print(f"load_data(): Collection '{self.collection}' exists.")
            else:
                print(f"load_data(): Collection '{self.collection}' does not exist.")

            collection = self.db[self.collection]

            # Fetch and return the data from the collection
            data = list(collection.find())

            return data

        except (ConnectionFailure, PyMongoError) as e:
            print(f"load_data(): Error loading data from MongoDB: {e}")
            raise

    def upsert_data(self, data, key_field: str = '_id'):
        """
        Method that stores the data into the specified collection based on the connection source.

        :param data: Data to store into MongoDB source.
        :param key_field: key id specified for MongoDB.
        :return: Collection of data from the MongoDB source.
        """

        try:
            if self.collection in self.db.list_collection_names():
                print(f"upsert_data(): Collection '{self.collection}' exists.")
            else:
                print(f"upsert_data(): Collection '{self.collection}' does not exist. New collection will be created.")

            collection = self.db[self.collection]
            for document in tqdm(data, desc="Writing to mongoDB", unit="document"):
                collection.update_one(
                    {key_field: document[key_field]},
                    {'$set': document},
                    upsert=True
                )

        except (ConnectionFailure, PyMongoError) as e:
            print(f"upsert_data(): Error inserting data into MongoDB: {e}")
            raise

    def delete_data(self, key_value: str, key_field: str = '_id'):
        """
        Deletes a document from the specified collection based on a key field.

        :param key_value: The value of the key field to identify the document to delete.
        :param key_field: The field used to uniquely identify the document for deletion
                          (default is "_id").
        :return: The result of the delete operation.
        """
        try:
            if self.collection in self.db.list_collection_names():
                print(f"delete_data(): Collection '{self.collection}' exists.")
            else:
                print(f"delete_data(): Collection '{self.collection}' does not exist.")
                return None

            collection = self.db[self.collection]

            result = collection.delete_one({key_field: key_value})

            if result.deleted_count == 1:
                print(f"delete_data(): Successfully deleted document with {key_field} = {key_value}.")
            else:
                print(f"delete_data(): No document found with {key_field} = {key_value}.")

            return result

        except (ConnectionFailure, PyMongoError) as e:
            print(f"delete_data(): Error deleting data from MongoDB: {e}")
            raise

    def close(self):
        """
        Method to close connection to current Mongo Client.
        """
        self.client.close()
