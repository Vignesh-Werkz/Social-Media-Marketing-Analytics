"""Module for Test DataClientManager"""
import unittest
from unittest.mock import patch, MagicMock
from src.datamanagement.dataclient import DataClientManager, DataClientConfig, MongoDBClient


class TestDataClientManager(unittest.TestCase):
    """
    Test class for DataClientManager and MongoDBClient Unit Testing.
    """

    @patch("src.datamanagement.dataclient.mongodb_client.MongoClient")
    def test_get_mongodb_client(self, mock_mongo_client):
        """
        Method to test that MongoDB client is returned based on db_type, without opening a real connection.
        """
        # Mock the MongoClient to prevent actual connection attempts
        mock_client_instance = MagicMock()
        mock_mongo_client.return_value = mock_client_instance

        # Create a mock DataClientConfig for MongoDB
        config = DataClientConfig(db_type="mongodb", uri="mongodb://localhost",
                                  db_name="test_db", collection="test_collection")

        # Test that the correct client (MongoDBClient) is returned
        client = MongoDBClient(config)
        self.assertIsInstance(client, MongoDBClient)

        # Check that the mocked MongoClient was called with the correct URI
        mock_mongo_client.assert_called_with("mongodb://localhost")

        # Close the client (it is mocked, so no actual connection is closed)
        client.close()

        # Ensure that the close method was called on the mocked client
        mock_client_instance.close.assert_called_once()

    def test_unsupported_db_type(self):
        """
        Method to test error raised for unsupported database type.
        """
        config = DataClientConfig(
            db_type="sql", uri="sql://localhost", db_name="test_db", collection="test_collection")
        with self.assertRaises(ValueError):
            DataClientManager.get_database_client(config)


if __name__ == '__main__':
    unittest.main()
