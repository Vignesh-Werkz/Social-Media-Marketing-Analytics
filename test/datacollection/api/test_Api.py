import unittest
from src.datacollection.api.Api import Api

class test_Api(unittest.TestCase):
    """
    Unit Tests for the Api class.
    """
    def test_init_cannotInstantiateAbstractClass(self):
        """
        Test that the Api class cannot be instantiated.
        """
        self.assertRaises(TypeError, Api)
