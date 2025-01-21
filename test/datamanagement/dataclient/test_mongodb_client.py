"""Module for Test MongoDBClient"""
import unittest
from unittest.mock import patch, MagicMock
from src.datamanagement.dataclient import MongoDBClient, DataClientConfig


class TestMongoDBClient(unittest.TestCase):
    """
    Test class for MongoDBClient Unit Testing.
    """
    # pylint: disable=arguments-differ, unused-variable, too-few-public-methods

    @patch("src.datamanagement.dataclient.mongodb_client.MongoClient")
    def setUp(self, mock_mongo_client):
        """
        Set up method for defining common test variables and mock objects.
        """
        # Mock collection and database
        self.mock_client = MagicMock()
        self.mock_collection = MagicMock()
        self.mock_db = MagicMock()

        # Set up mock return values
        mock_mongo_client.return_value = self.mock_client
        self.mock_client.__getitem__.return_value = self.mock_db
        self.mock_db.__getitem__.return_value = self.mock_collection

        # Set up configuration and MongoDBClient
        self.config = DataClientConfig(
            db_type="mongodb", uri="mongodb://localhost", db_name="test_db", collection="test_collection"
        )
        self.client = MongoDBClient(self.config)
        self.mock_collection.find.return_value = [
            {"_id": 1, "value": "test"}
        ]

    def test_load_data(self):
        """
        Method to test data loading from MongoDB.
        """
        # Mock the find method to return specific data
        self.mock_collection.find.return_value = [{"_id": 1, "value": "test"}]

        # Call the load_data method and assert the expected result
        data = self.client.load_data()
        self.assertEqual(data, [{"_id": 1, "value": "test"}])

    def test_upsert_data(self):
        """
        Method to test upserting data to MongoDB.
        """
        # Call the upsert_data method
        self.client.upsert_data([{"_id": 1, "value": "test"}])

        # Check that update_one was called with the expected parameters
        self.mock_collection.update_one.assert_called_with(
            {"_id": 1}, {"$set": {"_id": 1, "value": "test"}}, upsert=True
        )

    def test_ping_server_success(self):
        """
        Method to test successful connection to MongoDB.
        """
        with patch("src.datamanagement.dataclient.mongodb_client.MongoClient") as mock_mongo_client:
            mock_mongo_client.return_value.admin.command.return_value = {
                "ok": 1}
            client = MongoDBClient(self.config)
            self.assertEqual(client.client.admin.command('ping'), {"ok": 1})

    def test_ping_server_failure(self):
        """
        Method to test failure in connecting to MongoDB.
        """
        with patch("src.datamanagement.dataclient.mongodb_client.MongoClient") as mock_mongo_client:
            mock_mongo_client.return_value.admin.command.side_effect = Exception(
                "Connection failed")
            with self.assertRaises(Exception):
                MongoDBClient(self.config)

    def test_close(self):
        """
        Method to test closing of MongoDB client connection.
        """
        with patch("src.datamanagement.dataclient.mongodb_client.MongoClient") as mock_mongo_client:
            # Create a mock client
            mock_client_instance = MagicMock()
            mock_mongo_client.return_value = mock_client_instance

            # Create a MongoDBClient instance
            client = MongoDBClient(self.config)

            # Call the close method
            client.close()

            # Check that the mock client's close method was called
            mock_client_instance.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
