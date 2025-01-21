"""Module for Test DataClientConfig"""
import unittest
from src.datamanagement.dataclient import DataClientConfig


class TestDataClientConfig(unittest.TestCase):
    """
    Test class for DataClientConfig Unit Testing.
    """

    def test_config_initialization(self):
        """
        Method to test initialization of DataClientConfig.
        """
        config = DataClientConfig(db_type="mongodb", uri="mongodb://localhost", 
                                  db_name="test_db", collection="test_collection")
        self.assertEqual(config.db_type, "mongodb")
        self.assertEqual(config.uri, "mongodb://localhost")
        self.assertEqual(config.db_name, "test_db")
        self.assertEqual(config.collection, "test_collection")


if __name__ == '__main__':
    unittest.main()
