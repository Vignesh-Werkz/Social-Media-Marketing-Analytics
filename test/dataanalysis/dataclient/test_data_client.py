import unittest
from unittest.mock import MagicMock
from src.dataanalysis.dataclient.data_client import DataClient


class TestDataClient(unittest.TestCase):

    def setUp(self):
        self.mock_client = MagicMock(spec=DataClient)

    def test_load_data(self):
        self.mock_client.load_data.return_value = [{"_id": 1, "name": "Test"}]

        result = self.mock_client.load_data(filters={"name": "Test"})
        self.mock_client.load_data.assert_called_once_with(filters={"name": "Test"})
        self.assertEqual(result, [{"_id": 1, "name": "Test"}])

    def test_upsert_data(self):
        data = [{"_id": 1, "name": "Test"}]
        self.mock_client.upsert_data(data, key_field="_id")
        self.mock_client.upsert_data.assert_called_once_with(data, key_field="_id")

    def test_close(self):
        self.mock_client.close()
        self.mock_client.close.assert_called_once()
