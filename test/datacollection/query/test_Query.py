import unittest
from src.datacollection.query.Query import Query

class test_Query(unittest.TestCase):
    """
    Unit Tests for the Query
    """
    def test_init_cannotInstantiateAbstractClass(self):
        """
        Test that the Query class cannot be instantiated.
        """
        self.assertRaises(TypeError, Query)