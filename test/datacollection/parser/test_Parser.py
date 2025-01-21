import unittest
from src.datacollection.parser.Parser import Parser

class test_Parser(unittest.TestCase):
    """
    Unit Tests for the Parser class.
    """
    def test_init_cannotInstantiateAbstractClass(self):
        """
        Test that the Parser class cannot be instantiated.
        """
        self.assertRaises(TypeError, Parser)