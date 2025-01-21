"""Module for DataClient."""
from abc import ABC, abstractmethod


class DataClient(ABC):
    """
    Abstract class for database clients, providing a unified interface 
    for different databases.
    """

    @abstractmethod
    def load_data(self):
        """
        Loads data from the specified collection in the database.

        In the context of NoSQL databases like MongoDB:
        - A **collection** is similar to a table in relational databases (like MySQL or PostgreSQL).
        - It holds documents (or records) related to a specific entity.

        Example in MongoDB:
        - If the `collection_name` is "users", this method will load data from the "users" 
          collection, which stores documents representing user data.

        :param collection_name: The name of the collection (e.g., "users", "orders") 
                                from which data will be loaded.
        :return: A list of documents (records) from the specified collection.
        """

    @abstractmethod
    def upsert_data(self, data, key_field: str = '_id'):
        """
        Inserts or updates data in the specified collection of the database.

        In MongoDB (and similar NoSQL databases), this method will:
        - Insert new documents if they don't exist.
        - Update existing documents if they do exist, using a unique field such as 
          `_id` or another key field.

        Example:
        - If `collection_name` is "users" and `key_field` is "_id", this method will
          upsert (update or insert) documents in the "users" collection based on the `_id` field.

        :param collection_name: The name of the collection (e.g., "users", "products") 
                                where data will be inserted or updated.
        :param data: The data to be inserted or updated (usually in the form of a 
                     list of documents).
        :param key_field: The field used to uniquely identify documents for updating 
                          (default is "_id").
        """

    @abstractmethod
    def close(self):
        """
        Closes the database connection.

        This method ensures that the connection to the database (e.g., MongoDB) is properly
        closed after data operations are complete, releasing any resources or connections 
        used during the process.
        """
