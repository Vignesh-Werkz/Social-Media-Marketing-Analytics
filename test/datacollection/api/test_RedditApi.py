import unittest
from src.datacollection.api.RedditApi import RedditApi

class test_RedditApi(unittest.TestCase):
    # Sprint 4 Task - Ask Prof. about API testing practices.
    """
    Unit Tests for the RedditApi class.
    """
    def test_init_cannotInstantiateAbstractClass(self):
        """
        Test that the RedditApi class cannot be instantiated.
        """
        self.assertRaises(TypeError, RedditApi)