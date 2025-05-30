import unittest
import pandas as pd
import numpy as np
from io import StringIO
from your_module import analyze_distributions, generate_distribution_html

class TestDistributionAnalysis(unittest.TestCase):
    def setUp(self):
        # �������� ������
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
        """���� ������� ����������� �������������"""
        result = analyze_distributions(self.normal_data)
        
        self.assertIn('normal_col', result)
        stats = result['normal_col']['stats']
        
        # �������� �������� ���������
        self.assertAlmostEqual(stats['mean'], 0, delta=0.5)
        self.assertAlmostEqual(stats['median'], 0, delta=0.5)
        self.assertAlmostEqual(stats['std'], 1, delta=0.5)
        
        # �������� ������������
        self.assertTrue(stats['is_normal'])
        self.assertGreater(stats['shapiro_p'], 0.05)
        
        # �������� ��������
        self.assertEqual(stats['outliers_count'], 0)

    def test_skewed_distribution(self):
        """���� ������� ���������� �������������"""
        result = analyze_distributions(self.skewed_data)
        
        self.assertIn('skewed_col', result)
        stats = result['skewed_col']['stats']
        
        # �������� ������������
        self.assertFalse(stats['is_normal'])
        if stats['shapiro_p'] is not None:
            self.assertLessEqual(stats['shapiro_p'], 0.05)
        
        # �������� ����������
        self.assertGreater(stats['skewness'], 0.5)

    def test_empty_dataframe(self):
        """���� � ������ DataFrame"""
        result = analyze_distributions(self.empty_df)
        self.assertEqual(result, {})

    def test_mixed_data_types(self):
        """���� � DataFrame, ���������� ������ ���� ������"""
        result = analyze_distributions(self.mixed_df)
        
        # ���������, ��� ��������������� ������ �������� �������
        self.assertIn('numeric1', result)
        self.assertIn('numeric2', result)
        self.assertNotIn('text_col', result)
        
        # �������� ��������� ��� numeric1
        stats1 = result['numeric1']['stats']
        self.assertEqual(stats1['mean'], 3)
        self.assertEqual(stats1['median'], 3)
        self.assertEqual(stats1['outliers_count'], 0)

    def test_outlier_detection(self):
        """���� ����������� ��������"""
        result = analyze_distributions(self.with_outliers)
        stats = result['outlier_col']['stats']
        
        self.assertEqual(stats['outliers_count'], 1)
        self.assertAlmostEqual(stats['outliers_percent'], 16.67, delta=0.01)

    def test_generate_html_normal(self):
        """���� ��������� HTML ��� ����������� �������������"""
        html = generate_distribution_html(self.normal_data)
        self.assertIn('normal_col', html)
        self.assertIn('data:image/png;base64', html)
        self.assertIn('���������� �������������?', html)
        self.assertIn('��', html)

    def test_generate_html_skewed(self):
        """���� ��������� HTML ��� ���������� �������������"""
        html = generate_distribution_html(self.skewed_data)
        self.assertIn('skewed_col', html)
        self.assertIn('���', html)

    def test_generate_html_empty(self):
        """���� ��������� HTML ��� ������� DataFrame"""
        html = generate_distribution_html(self.empty_df)
        self.assertIn('��� �������� �������� ��� �������', html)

    def test_generate_html_with_outliers(self):
        """���� ��������� HTML � ���������"""
        html = generate_distribution_html(self.with_outliers)
        self.assertIn('outlier_col', html)
        self.assertIn('16.67%', html)

if __name__ == '__main__':
    unittest.main()