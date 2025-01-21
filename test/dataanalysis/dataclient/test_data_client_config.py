import unittest
from src.dataanalysis.dataclient.data_client_config import DataClientConfig


class TestDataClientConfig(unittest.TestCase):

    def test_initialization(self):
        config = DataClientConfig(db_type="MongoDB", uri="mongodb://localhost:27017", db_name="test_db",
                                  collection="users")

        self.assertEqual(config.db_type, "MongoDB")
        self.assertEqual(config.uri, "mongodb://localhost:27017")
        self.assertEqual(config.db_name, "test_db")
        self.assertEqual(config.collection, "users")

    def test_invalid_initialization(self):
        with self.assertRaises(TypeError):
            DataClientConfig(db_type="MongoDB", uri="mongodb://localhost:27017",
                             db_name="test_db")
