"""Module for Test TextCleaning Filter."""
import unittest
from src.datamanagement.filters import Pipe, TextCleaningFilter


class TestTextCleaningFilter(unittest.TestCase):
    """
    Test class for TextCleaning Filter Unit Testing.
    """
    # pylint: disable=abstract-class-instantiated, unused-variable, too-few-public-methods

    def setUp(self):
        """
        Set up method to define test variables.
        """
        self.pipe = Pipe()
        self.test_data = [{"selftext": "This is a TEST!", "title": "Test TITLE",
                           "comments": ["Great Post!"]}]
        self.empty_data = [{"selftext": "", "title": "", "comments": [""]}]
        self.special_data = [{"selftext": "Hello@world!!!", "title": "Title$^&",
                        "comments": ["Comment*&%"]}]
        self.short_data = [{"selftext": "Hi", "title": "A", "comments": ["!"]}]
        long_text = "a" * 10000
        self.long_data = [{"selftext": long_text, "title": long_text, 
                           "comments": [long_text]}]
        self.filter = TextCleaningFilter()

    def test_valid_text(self):
        """
        Method to test and ensure special characters are removed.
        """
        self.pipe.set_data(self.test_data)
        self.filter.execute(self.pipe)
        cleaned_data = self.pipe.get_data()
        for post in cleaned_data:
            self.assertNotIn('!', post['transformed_data']['selftext'])

    def test_empty_text(self):
        """
        Method to test empty data cleaning.
        """
        self.pipe.set_data(self.empty_data)
        self.filter.execute(self.pipe)
        cleaned_data = self.pipe.get_data()
        self.assertEqual(cleaned_data[0]['transformed_data']['selftext'], "")
        self.assertEqual(cleaned_data[0]['transformed_data']['title'], "")
        self.assertEqual(cleaned_data[0]['transformed_data']['comments'], [""])

    def test_special_text(self):
        """
        Method to test special character data cleaning.
        """
        self.pipe.set_data(self.special_data)
        self.filter.execute(self.pipe)
        cleaned_data = self.pipe.get_data()
        self.assertEqual(cleaned_data[0]['transformed_data']['selftext'], "hello world")
        self.assertEqual(cleaned_data[0]['transformed_data']['title'], "title")
        self.assertEqual(cleaned_data[0]['transformed_data']['comments'], ["comment"])

    def test_short_text(self):
        """
        Method to test short character data cleaning.
        """
        self.pipe.set_data(self.short_data)
        self.filter.execute(self.pipe)
        cleaned_data = self.pipe.get_data()
        self.assertEqual(cleaned_data[0]['transformed_data']['selftext'], "hi")
        self.assertEqual(cleaned_data[0]['transformed_data']['title'], "a")
        self.assertEqual(cleaned_data[0]['transformed_data']['comments'], [""])

    def test_long_text(self):
        """
        Method to test long character data cleaning.
        """
        self.pipe.set_data(self.long_data)
        self.filter.execute(self.pipe)
        cleaned_data = self.pipe.get_data()
        self.assertEqual(len(cleaned_data[0]['transformed_data']['selftext']), 10000)
        self.assertEqual(len(cleaned_data[0]['transformed_data']['title']), 10000)
        self.assertEqual(len(cleaned_data[0]['transformed_data']['comments'][0]), 10000)

if __name__ == '__main__':
    unittest.main()
