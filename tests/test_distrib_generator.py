import unittest
import pandas as pd
import numpy as np
from io import StringIO
from your_module import analyze_distributions, generate_distribution_html

class TestDistributionAnalysis(unittest.TestCase):
    def setUp(self):
        # Тестовые данные
        self.normal_data = pd.DataFrame({
            'normal_col': np.random.normal(0, 1, 100)
        })
        
        self.skewed_data = pd.DataFrame({
            'skewed_col': np.random.exponential(1, 100)
        })
        
        self.empty_df = pd.DataFrame()
        
        self.mixed_df = pd.DataFrame({
            'numeric1': [1, 2, 3, 4, 5],
            'numeric2': [10, 20, 30, 40, 50],
            'text_col': ['a', 'b', 'c', 'd', 'e']
        })
        
        self.with_outliers = pd.DataFrame({
            'outlier_col': [1, 2, 3, 4, 5, 100]
        })

    def test_normal_distribution(self):
        """Тест анализа нормального распределения"""
        result = analyze_distributions(self.normal_data)
        
        self.assertIn('normal_col', result)
        stats = result['normal_col']['stats']
        
        # Проверка основных статистик
        self.assertAlmostEqual(stats['mean'], 0, delta=0.5)
        self.assertAlmostEqual(stats['median'], 0, delta=0.5)
        self.assertAlmostEqual(stats['std'], 1, delta=0.5)
        
        # Проверка нормальности
        self.assertTrue(stats['is_normal'])
        self.assertGreater(stats['shapiro_p'], 0.05)
        
        # Проверка выбросов
        self.assertEqual(stats['outliers_count'], 0)

    def test_skewed_distribution(self):
        """Тест анализа скошенного распределения"""
        result = analyze_distributions(self.skewed_data)
        
        self.assertIn('skewed_col', result)
        stats = result['skewed_col']['stats']
        
        # Проверка нормальности
        self.assertFalse(stats['is_normal'])
        if stats['shapiro_p'] is not None:
            self.assertLessEqual(stats['shapiro_p'], 0.05)
        
        # Проверка асимметрии
        self.assertGreater(stats['skewness'], 0.5)

    def test_empty_dataframe(self):
        """Тест с пустым DataFrame"""
        result = analyze_distributions(self.empty_df)
        self.assertEqual(result, {})

    def test_mixed_data_types(self):
        """Тест с DataFrame, содержащим разные типы данных"""
        result = analyze_distributions(self.mixed_df)
        
        # Проверяем, что анализировались только числовые столбцы
        self.assertIn('numeric1', result)
        self.assertIn('numeric2', result)
        self.assertNotIn('text_col', result)
        
        # Проверка статистик для numeric1
        stats1 = result['numeric1']['stats']
        self.assertEqual(stats1['mean'], 3)
        self.assertEqual(stats1['median'], 3)
        self.assertEqual(stats1['outliers_count'], 0)

    def test_outlier_detection(self):
        """Тест обнаружения выбросов"""
        result = analyze_distributions(self.with_outliers)
        stats = result['outlier_col']['stats']
        
        self.assertEqual(stats['outliers_count'], 1)
        self.assertAlmostEqual(stats['outliers_percent'], 16.67, delta=0.01)

    def test_generate_html_normal(self):
        """Тест генерации HTML для нормального распределения"""
        html = generate_distribution_html(self.normal_data)
        self.assertIn('normal_col', html)
        self.assertIn('data:image/png;base64', html)
        self.assertIn('Нормальное распределение?', html)
        self.assertIn('Да', html)

    def test_generate_html_skewed(self):
        """Тест генерации HTML для скошенного распределения"""
        html = generate_distribution_html(self.skewed_data)
        self.assertIn('skewed_col', html)
        self.assertIn('Нет', html)

    def test_generate_html_empty(self):
        """Тест генерации HTML для пустого DataFrame"""
        html = generate_distribution_html(self.empty_df)
        self.assertIn('Нет числовых столбцов для анализа', html)

    def test_generate_html_with_outliers(self):
        """Тест генерации HTML с выбросами"""
        html = generate_distribution_html(self.with_outliers)
        self.assertIn('outlier_col', html)
        self.assertIn('16.67%', html)

if __name__ == '__main__':
    unittest.main()