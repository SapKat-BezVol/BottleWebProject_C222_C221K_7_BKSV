import unittest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock
from services.prediction_generator import build_prediction_numbers

class TestPredictionGenerator(unittest.TestCase):

    def setUp(self):
        # Наборы тестовых DataFrame'ов
        self.datasets = {
            "simple_linear": pd.DataFrame({
                "feature": [1, 2, 3, 4, 5],
                "target": [2, 4, 6, 8, 10]  # y = 2x
            }),
            "multi_feature": pd.DataFrame({
                "x1": [1, 2, 3, 4, 5],
                "x2": [0, 1, 0, 1, 0],
                "y": [1, 3, 3, 5, 5]  # y = x1 + x2
            }),
            "constant_target": pd.DataFrame({
                "a": [1, 2, 3, 4, 5],
                "b": [2, 4, 6, 8, 10],
                "c": [5, 5, 5, 5, 5]  # Константа
            })
        }

        # Мок для request.forms
        self.mock_request = MagicMock()
        
    def test_successful_prediction_simple(self):
        """Тест успешного предсказания для простого линейного случая"""
        df = self.datasets["simple_linear"]
        
        # Настраиваем мок для request.forms
        self.mock_request.forms.get.side_effect = [
            '2',  # target_col (второй столбец - 'target')
            '6'    # features (одно значение)
        ]
        
        # Подменяем глобальный request на наш мок
        import sys
        sys.modules['bottle'].request = self.mock_request
        
        result = build_prediction_numbers(df)
        
        self.assertIn("Результат предсказания", result)
        self.assertIn("Целевая переменная: target", result)
        self.assertIn("Прогнозируемое значение", result)
        self.assertNotIn("Ошибка", result)

    def test_successful_prediction_multi_feature(self):
        """Тест успешного предсказания для множества признаков"""
        df = self.datasets["multi_feature"]
        
        self.mock_request.forms.get.side_effect = [
            '3',  # target_col (третий столбец - 'y')
            '6 1' # features (два значения)
        ]
        
        import sys
        sys.modules['bottle'].request = self.mock_request
        
        result = build_prediction_numbers(df)
        
        self.assertIn("x1: 6.00", result)
        self.assertIn("x2: 1.00", result)
        self.assertIn("y", result)

    def test_invalid_target_column(self):
        """Тест обработки неверного номера целевого столбца"""
        df = self.datasets["simple_linear"]
        
        self.mock_request.forms.get.side_effect = [
            '10',  # Несуществующий столбец
            '5'
        ]
        
        import sys
        sys.modules['bottle'].request = self.mock_request
        
        result = build_prediction_numbers(df)
        
        self.assertIn("Ошибка", result)
        self.assertIn("Некорректный номер целевого столбца", result)

    def test_wrong_features_count(self):
        """Тест обработки неверного количества признаков"""
        df = self.datasets["multi_feature"]
        
        self.mock_request.forms.get.side_effect = [
            '3',
            '6'  # Должно быть 2 значения
        ]
        
        import sys
        sys.modules['bottle'].request = self.mock_request
        
        result = build_prediction_numbers(df)
        
        self.assertIn("Ожидается 2 признаков", result)
        self.assertIn("Ошибка", result)

    def test_non_numeric_features(self):
        """Тест обработки нечисловых значений признаков"""
        df = self.datasets["simple_linear"]
        
        self.mock_request.forms.get.side_effect = [
            '2',
            'abc'  # Не число
        ]
        
        import sys
        sys.modules['bottle'].request = self.mock_request
        
        result = build_prediction_numbers(df)
        
        self.assertIn("Ошибка", result)
        self.assertIn("could not convert string to float", result)

    def test_constant_target_prediction(self):
        """Тест предсказания для константной целевой переменной"""
        df = self.datasets["constant_target"]
        
        self.mock_request.forms.get.side_effect = [
            '3',  # target_col (столбец 'c')
            '10 20'  # features (два значения)
        ]
        
        import sys
        sys.modules['bottle'].request = self.mock_request
        
        result = build_prediction_numbers(df)
        
        self.assertIn("Прогнозируемое значение: 5.0000", result)
