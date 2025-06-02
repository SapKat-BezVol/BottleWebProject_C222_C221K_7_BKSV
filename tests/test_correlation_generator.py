import unittest
import pandas as pd
from services.correlation_generator import (
    build_correlation_table,
    build_correlation_heatmap,
    analyze_correlations
)

class TestCorrelationGenerator(unittest.TestCase):

    def setUp(self):
        # Наборы тестовых DataFrame'ов
        self.datasets = {
            "positive_correlation": pd.DataFrame({
                "X": [1, 2, 3, 4, 5],
                "Y": [2, 4, 6, 8, 10],  # r = 1.0
            }),
            "negative_correlation": pd.DataFrame({
                "A": [1, 2, 3, 4, 5],
                "B": [10, 8, 6, 4, 2],  # r = -1.0
            }),
            "no_correlation": pd.DataFrame({
                "P": [1, 2, 3, 4, 5],
                "Q": [7, 9, 6, 8, 5],  # r ≈ 0
            }),
            "constant_column": pd.DataFrame({
                "C": [3, 3, 3, 3, 3],
                "D": [1, 2, 3, 4, 5],
            }),
            "mixed": pd.DataFrame({
                "M": [1, 2, 3, 4, 5],
                "N": [2, 1, 2, 1, 2],
                "O": [1, 2, 3, 4, 5],
            })
        }

    def test_build_correlation_table_html_structure(self):
        for name, df in self.datasets.items():
            with self.subTest(name=name):
                html = build_correlation_table(df)
                self.assertIn("<table", html)
                self.assertIn("Correlation Matrix", html)

    def test_analyze_correlations_output_contains_expected_phrases(self):
        expectations = {
            "positive_correlation": ["Сильная положительная корреляция"],
            "negative_correlation": ["Сильная отрицательная корреляция"],
            "no_correlation": ["Значимых корреляций не обнаружено."],
            "constant_column": ["Значимых корреляций не обнаружено."],
            "mixed": ["Сильная положительная корреляция"]
        }

        for name, df in self.datasets.items():
            with self.subTest(name=name):
                result = analyze_correlations(df)
                for phrase in expectations[name]:
                    self.assertIn(phrase, result)

    def test_build_correlation_heatmap_returns_img_tag(self):
        for name, df in self.datasets.items():
            with self.subTest(name=name):
                heatmap_html = build_correlation_heatmap(df)
                self.assertIn("<img", heatmap_html)
                self.assertIn("base64", heatmap_html)

if __name__ == "__main__":
    unittest.main()