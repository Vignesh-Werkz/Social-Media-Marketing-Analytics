"""Module for Test DataClient"""
import unittest
from src.datamanagement.dataclient import DataClient

class TestDataClient(unittest.TestCase):
    """
    Test class for DataClient Unit Testing.
    """
    # pylint: disable=abstract-class-instantiated, unused-variable, too-few-public-methods

    def test_cannot_instantiate_data_client(self):
        """
        Method to test that instantiating the abstract DataClient class raises an error.
        """
        with self.assertRaises(TypeError):
            client_instance = DataClient()

    def test_subclass_implements_methods(self):
        """
        Method to test that the subclass can be instantiated and the abstract methods work.
        """
        # Create a mock subclass for testing
        class MockDataClient(DataClient):
            """
            Mock DataClient Class.
            """

            def load_data(self):
                return [{"_id": 1, "value": "test"}]

            def upsert_data(self, data, key_field='_id'):
                pass

            def close(self):
                pass

        try:
            client_instance = MockDataClient()
            self.assertIsInstance(client_instance, MockDataClient)
        except TypeError as e:
            self.fail(f"Mock DataClient subclass instantiation failed: {e}")

    def test_subclass_methods(self):
        """
        Method to test that the mock subclass can call the abstract methods.
        """
        class MockDataClient(DataClient):
            """
            Mock DataClient Class.
            """

            def load_data(self):
                return [{"_id": 1, "value": "test"}]

            def upsert_data(self, data, key_field='_id'):
                pass

            def close(self):
                pass

        client_instance = MockDataClient()
        self.assertEqual(client_instance.load_data(), [
                         {"_id": 1, "value": "test"}])
        client_instance.upsert_data([{"_id": 1, "value": "test"}])
        client_instance.close()


if __name__ == '__main__':
    unittest.main()
