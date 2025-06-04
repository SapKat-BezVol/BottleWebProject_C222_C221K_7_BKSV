import unittest
import pandas as pd
import numpy as np
from generators.distrib_generator import analyze_distributions, generate_distribution_html

class TestDistribGenerator(unittest.TestCase):
    def setUp(self):
        """Подготовка тестовых данных"""
        # Нормальное распределение
        self.normal_data = pd.DataFrame({
            'normal': np.random.normal(0, 1, 1000)
        })
        
        # Экспоненциальное распределение
        self.exp_data = pd.DataFrame({
            'exp': np.random.exponential(1, 1000)
        })
        
        # Пустые данные
        self.empty_df = pd.DataFrame()
        
        # Данные без числовых столбцов
        self.non_numeric_df = pd.DataFrame({
            'text': ['a', 'b', 'c'],
            'bool': [True, False, True]
        })
        
        # Данные с пропусками
        self.data_with_nans = pd.DataFrame({
            'with_nans': [1, 2, np.nan, 4, 5, np.nan, 7]
        })
        
        # Маленький набор данных
        self.small_data = pd.DataFrame({
            'small': [1, 2, 3]
        })
    
    def test_analyze_non_normal_distribution(self):
        """Тест анализа ненормального распределения"""
        result = analyze_distributions(self.exp_data)
        self.assertIn('exp', result)
        self.assertFalse(result['exp']['stats']['is_normal'])
        self.assertGreater(result['exp']['stats']['skewness'], 1)  # Ожидаем положительную асимметрию
    
    def test_empty_dataframe(self):
        """Тест с пустым DataFrame"""
        result = analyze_distributions(self.empty_df)
        self.assertEqual(len(result), 0)
        
        html_result = generate_distribution_html(self.empty_df)
        self.assertIn('alert-warning', html_result)
    
    def test_non_numeric_data(self):
        """Тест с DataFrame без числовых столбцов"""
        result = analyze_distributions(self.non_numeric_df)
        self.assertEqual(len(result), 0)
        
        html_result = generate_distribution_html(self.non_numeric_df)
        self.assertIn('alert-warning', html_result)
    
    def test_data_with_nans(self):
        """Тест обработки данных с пропусками"""
        result = analyze_distributions(self.data_with_nans)
        self.assertIn('with_nans', result)
        self.assertEqual(result['with_nans']['stats']['outliers_count'], 0)  # В этом наборе не должно быть выбросов
    
    def test_generate_html_structure(self):
        """Тест структуры генерируемого HTML"""
        html_result = generate_distribution_html(self.normal_data)
        self.assertIn('<div class=\'card mb-4\'>', html_result)
        self.assertIn('<table class=\'table table-bordered\'>', html_result)
        self.assertIn('base64', html_result)  # Проверяем наличие закодированных изображений
    
    def test_outliers_detection(self):
        """Тест обнаружения выбросов"""
        test_data = pd.DataFrame({
            'with_outliers': [1, 2, 3, 4, 5, 100]  # 100 - явный выброс
        })
        result = analyze_distributions(test_data)
        self.assertEqual(result['with_outliers']['stats']['outliers_count'], 1)
        self.assertAlmostEqual(result['with_outliers']['stats']['outliers_percent'], 16.67, delta=0.1)

if __name__ == '__main__':
    unittest.main()