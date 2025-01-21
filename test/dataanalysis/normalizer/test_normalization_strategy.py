import unittest
from src.dataanalysis.normalizer.normalization_strategy import MinMaxNormalizationStrategy


class TestMinMaxNormalizationStrategy(unittest.TestCase):
    def setUp(self):
        self.min_max_normalizer = MinMaxNormalizationStrategy(min_value=-1, max_value=1)

    def test_normalize_single_value(self):
        result = self.min_max_normalizer.normalize(0)
        self.assertEqual(result, 50.0)

    def test_normalize_list_of_values(self):
        result = self.min_max_normalizer.normalize([-1, 0, 1])
        self.assertEqual(result, [0.0, 50.0, 100.0])  # -1 -> 0, 0 -> 50, 1 -> 100

    def test_normalize_with_custom_range(self):
        result = self.min_max_normalizer.normalize(0)
        self.assertEqual(result, 50.0)

    def test_normalize_min_equals_max(self):
        strategy = MinMaxNormalizationStrategy(min_value=0, max_value=0)
        with self.assertRaises(ZeroDivisionError):
            strategy.normalize(50)

    def test_normalize_empty_list(self):
        result = self.min_max_normalizer.normalize([])
        self.assertEqual(result, [])

    def test_normalize_invalid_type(self):
        with self.assertRaises(TypeError):
            self.min_max_normalizer.normalize("invalid_input")

    def test_normalize_None(self):
        with self.assertRaises(TypeError):
            self.min_max_normalizer.normalize(None)
