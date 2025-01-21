"""Module for Test Pipe"""
import unittest
from src.datamanagement.filters import Pipe


class TestPipe(unittest.TestCase):
    """
    Test class for Pipe Unit Testing.
    """
    # pylint: disable=abstract-class-instantiated, unused-variable, too-few-public-methods

    def setUp(self):
        self.pipe = Pipe()
        self.test_data = [
            {
                "selftext": "This is a test",
                "title": "Test Title",
                "comments": ["Great post!"]
            }
        ]
        self.empty_data = []
        self.initial_data = [{"selftext": "Initial Data"}]
        self.new_data = [{"selftext": "New Data"}]
        self.large_data = [
            {
                "selftext": "Text " * 1000,
                "title": "Title " * 1000,
                "comments": ["Comment " * 1000]
            }
        ]

    def test_set_and_get_data(self):
        """
        Method to test setting and getting data.
        """
        self.pipe.set_data(self.test_data)
        # Check that the data is properly stored and can be retrieved
        retrieved_data = self.pipe.get_data()
        self.assertEqual(retrieved_data, self.test_data)

    def test_empty_data(self):
        """
        Method to test setting and getting empty data.
        """
        self.pipe.set_data(self.empty_data)

        # Check that an empty list is handled gracefully
        retrieved_data = self.pipe.get_data()
        self.assertEqual(retrieved_data, [])

    def test_overwrite_data(self):
        """
        Method to test setting new and update data.
        """
        # Set initial data and then overwrite it
        self.pipe.set_data(self.initial_data)
        self.pipe.set_data(self.new_data)

        # Ensure the data was overwritten
        retrieved_data = self.pipe.get_data()
        self.assertEqual(retrieved_data, self.new_data)

    def test_large_data(self):
        """
        Method to test setting large data.
        """
        # Test handling of large data sets
        self.pipe.set_data(self.large_data)

        # Ensure the pipe can handle large data sets
        retrieved_data = self.pipe.get_data()
        self.assertEqual(retrieved_data, self.large_data)


if __name__ == '__main__':
    unittest.main()
