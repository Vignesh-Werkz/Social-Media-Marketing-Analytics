import unittest
from src.dataanalysis.normalizer import VADERNormalizer, TextBlobNormalizer


class TestVADERNormalizer(unittest.TestCase):
    def setUp(self):
        self.vader_normalizer = VADERNormalizer()

    def test_normalize_vader_scores(self):

        data = {
            "title_sentiment": 0.4,
            "selftext_sentiment": 0.5,
            "comment_sentiment": [0.3, -1.0, 0.2]
        }

        expected = {
            "title_sentiment": 70.0,
            "selftext_sentiment": 75.0,
            "comment_sentiment": [65.0, 0.0, 60.0]
        }

        result = self.vader_normalizer.normalize(data)

        self.assertAlmostEqual(result["title_sentiment"], expected["title_sentiment"], places=5)
        self.assertAlmostEqual(result["selftext_sentiment"], expected["selftext_sentiment"], places=5)

        for i in range(len(expected["comment_sentiment"])):
            self.assertAlmostEqual(result["comment_sentiment"][i], expected["comment_sentiment"][i], places=5)

    def test_vader_single_value(self):
        data = {"sentiment": 0.5}
        result = self.vader_normalizer.normalize(data)
        self.assertEqual(result["sentiment"], 75.0)

    def test_vader_list_values(self):
        data = {"sentiments": [-1, 0, 1]}
        result = self.vader_normalizer.normalize(data)
        self.assertEqual(result["sentiments"], [0.0, 50.0, 100.0])

    def test_empty_dictionary(self):
        result = self.vader_normalizer.normalize({})
        self.assertEqual(result, {})

    def test_mixed_values(self):
        data = {"score1": -1, "score2": [0, 1, -1]}
        result = self.vader_normalizer.normalize(data)
        self.assertEqual(result["score1"], 0.0)
        self.assertEqual(result["score2"], [50.0, 100.0, 0.0])

    def test_min_max_boundary(self):
        data = {"score": [-1, 1]}
        result = self.vader_normalizer.normalize(data)
        self.assertEqual(result["score"], [0.0, 100.0])

    def test_out_of_bounds(self):
        data = {"score": [-1.1, 1.1]}
        result = self.vader_normalizer.normalize(data)
        self.assertAlmostEqual(result["score"][0], 0.0, places=5)
        self.assertAlmostEqual(result["score"][1], 100.0, places=5)


class TestTextBlobNormalizer(unittest.TestCase):
    def setUp(self):
        self.textblob_normalizer = TextBlobNormalizer()

    def test_normalize_textblob_scores(self):

        data = {
            "title_sentiment": -0.2,
            "selftext_sentiment": 0.8,
            "comment_sentiment": [0.1, 0.9, -0.5]
        }

        expected = {
            "title_sentiment": 40.0,
            "selftext_sentiment": 90.0,
            "comment_sentiment": [55.0, 95.0, 25.0]
        }

        result = self.textblob_normalizer.normalize(data)

        self.assertAlmostEqual(result["title_sentiment"], expected["title_sentiment"], places=5)
        self.assertAlmostEqual(result["selftext_sentiment"], expected["selftext_sentiment"], places=5)

        for i in range(len(expected["comment_sentiment"])):
            self.assertAlmostEqual(result["comment_sentiment"][i], expected["comment_sentiment"][i], places=5)

    def test_textblob_single_value(self):
        data = {"sentiment": -0.5}
        result = self.textblob_normalizer.normalize(data)
        self.assertEqual(result["sentiment"], 25.0)

    def test_textblob_list_values(self):
        data = {"sentiments": [-1, 0, 1]}
        result = self.textblob_normalizer.normalize(data)
        self.assertEqual(result["sentiments"], [0.0, 50.0, 100.0])

    def test_empty_dictionary(self):
        result = self.textblob_normalizer.normalize({})
        self.assertEqual(result, {})

    def test_mixed_values(self):
        data = {"score1": -1, "score2": [0, 1, -1]}
        result = self.textblob_normalizer.normalize(data)
        self.assertEqual(result["score1"], 0.0)
        self.assertEqual(result["score2"], [50.0, 100.0, 0.0])

    def test_min_max_boundary(self):
        data = {"score": [-1, 1]}
        result = self.textblob_normalizer.normalize(data)
        self.assertEqual(result["score"], [0.0, 100.0])

    def test_out_of_bounds(self):
        data = {"score": [-1.1, 1.1]}
        result = self.textblob_normalizer.normalize(data)
        self.assertAlmostEqual(result["score"][0], 0.0, places=5)
        self.assertAlmostEqual(result["score"][1], 100.0, places=5)

