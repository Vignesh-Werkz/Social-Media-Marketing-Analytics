"""Module for Test Transformation"""
import unittest
from src.datamanagement.transformationmodels.transformation import Transformation


class TestTransformation(unittest.TestCase):
    """
    Test class for Transformation Unit Testing.
    """
    # pylint: disable=abstract-class-instantiated, unused-variable, too-few-public-methods

    def test_cannot_instantiate_transformation(self):
        """
        Method to test that instantiating the abstract Transformation class raises an error.
        """
        with self.assertRaises(TypeError):
            transformation_instance = Transformation()

    def test_subclass_implements_methods(self):
        """
        Method to test that the subclass can be instantiated and the abstract methods work.
        """
        # Create a subclass for testing
        class MockTransformation(Transformation):
            """
            Mock subclass of Transformation for testing purposes.
            """
            def apply(self, data):
                return data  # Mock implementation for testing

        try:
            transformation_instance = MockTransformation()
            # Test that the subclass is created without errors
            self.assertIsInstance(transformation_instance, MockTransformation)
        except TypeError as e:
            self.fail(f"Mock Transformation subclass instantiation failed: {e}")

    def test_subclass_executes_apply(self):
        """
        Method to test a mock subclass of Transformation that implements the apply method.
        """
        class MockTransformation(Transformation):
            """
            Mock subclass of Transformation for testing purposes.
            """
            def apply(self, data):
                for post in data:
                    post["processed"] = True  # Mock processing step
                return data

        # Create mock data for testing
        mock_data = [{"selftext": "Some data", "title": "Some title", "comments": ["Comment 1"]}]

        # Instantiate the mock transformation subclass
        mock_transformation = MockTransformation()

        # Execute the apply method and check if it modifies the data after apply()
        result = mock_transformation.apply(mock_data)

        # Ensure the data is modified as expected
        self.assertEqual(result[0]["processed"], True)

if __name__ == '__main__':
    unittest.main()
