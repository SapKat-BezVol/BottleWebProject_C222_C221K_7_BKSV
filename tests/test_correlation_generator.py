import unittest
import pandas as pd
import numpy as np
from generators.correlation_generator import (
    build_correlation_table,
    build_correlation_heatmap,
    analyze_correlations,
)

class TestCorrelationGenerator(unittest.TestCase):

    def setUp(self):
        # Подготовка различных тестовых DataFrame'ов
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
        # Проверка, что функция возвращает HTML-таблицу с заголовком
        for name, df in self.datasets.items():
            with self.subTest(name=name):
                html = build_correlation_table(df)
                self.assertIn("<table", html)
                self.assertIn("Correlation Matrix", html)

    def test_analyze_correlations_output_contains_expected_phrases(self):
        # Проверка корректности текстового анализа корреляций
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
        # Проверка, что тепловая карта содержит <img> с base64
        for name, df in self.datasets.items():
            with self.subTest(name=name):
                heatmap_html = build_correlation_heatmap(df)
                self.assertIn("<img", heatmap_html)
                self.assertIn("base64", heatmap_html)

    def test_handle_empty_dataframe(self):
        # Проверка, что при пустом DataFrame возвращается сообщение, а не пустая таблица
        df = pd.DataFrame()
        table_html = build_correlation_table(df)
        heatmap_html = build_correlation_heatmap(df)
        result_text = analyze_correlations(df)

        self.assertIn("Нет данных для отображения корреляционной таблицы.", table_html)
        self.assertIn("Нет данных для отображения тепловой карты.", heatmap_html)
        self.assertIn("данных недостаточно", result_text.lower())


    def test_handle_nan_values(self):
        # Проверка, что NaN не вызывает ошибку при построении
        df = pd.DataFrame({
            "A": [1, 2, np.nan, 4, 5],
            "B": [5, np.nan, 3, 2, 1]
        })
        table_html = build_correlation_table(df)
        heatmap_html = build_correlation_heatmap(df)
        result_text = analyze_correlations(df)
        self.assertIn("<table", table_html)
        self.assertIn("<img", heatmap_html)
        self.assertIn("корреляция", result_text.lower())

    def test_correlation_table_shape(self):
        # Проверка, что таблица корреляции квадратная и по размеру как количество переменных
        df = self.datasets["positive_correlation"]
        corr = df.corr()
        self.assertEqual(corr.shape[0], corr.shape[1])
        self.assertEqual(corr.shape[0], len(df.columns))

    def test_correlation_diagonal_values(self):
        # Проверка, что на диагонали всегда стоит 1.0
        df = self.datasets["positive_correlation"]
        table_html = build_correlation_table(df)
        self.assertIn("1.0", table_html)  # Не "1.00", а "1.0"

if __name__ == "__main__":
    unittest.main()
