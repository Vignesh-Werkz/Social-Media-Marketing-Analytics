"""Module for Test Filter"""
import unittest
from src.datamanagement.filters import Pipe, Filter


class TestFilter(unittest.TestCase):
    """
    Test class for Filter Unit Testing.
    """
    # pylint: disable=abstract-class-instantiated, unused-variable, too-few-public-methods
    def test_cannot_instantiate_filter(self):
        """
        Method to test that instantiating the abstract Filter class raises an error.
        """
        with self.assertRaises(TypeError):
            filter_instance = Filter()

    def test_subclass_implements_methods(self):
        """
        Method to test that that the subclass can be instantiated and the abstract methods work.
        """
        # Create a subclass for testing
        class MockFilter(Filter):
            """
            Test Mock Class.
            """
            def execute(self, pipe: Pipe):
                pass  # Mock implementation for testing

        try:
            filter_instance = MockFilter()
            # Test that the subclass is created without errors
            self.assertIsInstance(filter_instance, MockFilter)
        except TypeError as e:
            self.fail(f"Mock Filter subclass instantiation failed: {e}")

    def test_subclass_executes_method(self):
        """
        Method to test a mock subclass of Filter that implements the execute method.
        """
        class MockFilter(Filter):
            """
            Test Mock Class.
            """
            def execute(self, pipe: Pipe):
                pipe.set_data([{"selftext": "mock data"}])  # Mock execution

        # Create a pipe object and mock data
        pipe = Pipe()
        mock_data = [{"selftext": "Some data", "title": "Some title", "comments": ["Comment 1"]}]
        pipe.set_data(mock_data)

        # Instantiate the mock filter subclass
        mock_filter = MockFilter()

        # Execute the filter and check if it modifies the data after execute()
        mock_filter.execute(pipe)
        data = pipe.get_data()

        # Ensure the data is modified as expected
        self.assertEqual(data[0]["selftext"], "mock data")

if __name__ == '__main__':
    unittest.main()
