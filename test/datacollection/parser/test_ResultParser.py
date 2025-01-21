import json
import unittest

from src.datacollection.parser.ResultParser import ResultParser

class test_ResultParser(unittest.TestCase):
    """
    Unit Tests for the ResultParser class.
    """
    def setUp(self):
        self.emptyDataList = []
        with open ("test/testdata/datacollection/ResultParserTest/RedditDataSingle.json") as jsonFile:
            self.singleDataList = json.load(jsonFile)
        with open ("test/testdata/datacollection/ResultParserTest/RedditDataMultiple.json") as jsonFile:
            self.multipleDataList = json.load(jsonFile)
        with open ("test/testdata/datacollection/ResultParserTest/RedditDataSingleExpected.json") as jsonFile:
            self.expectedSingleResult = jsonFile.read()
        with open ("test/testdata/datacollection/ResultParserTest/RedditDataMultipleExpected.json") as jsonFile:
            self.expectedMultipleResult = jsonFile.read()

    def test_parseRedditData_validData(self):
        """
        Test that the correct fields are extracted from Reddit data of varying sizes
        """
        # Test empty data list
        emptyResult = ResultParser.parseRedditData(self.emptyDataList)
        self.assertEqual(emptyResult, "[]")

        # Test single data list
        singleResult = ResultParser.parseRedditData(self.singleDataList)
        self.assertEqual(singleResult, self.expectedSingleResult)

        # Test multiple data list
        multipleResult = ResultParser.parseRedditData(self.multipleDataList)
        self.assertEqual(multipleResult, self.expectedMultipleResult)

    def test_parseRedditData_invalidData(self):
        """
        Test that the correct exceptions are raised for invalid data
        """
        # Test invalid data type
        with self.assertRaises(TypeError):
            ResultParser.parseRedditData("invalid data type")

        # None/Null data being passed to the parser
        with self.assertRaises(TypeError):
            ResultParser.parseRedditData(None)