import unittest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock
from services.prediction_generator import build_prediction_numbers

class TestPredictionGenerator(unittest.TestCase):

    def setUp(self):
        # ������ �������� DataFrame'��
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
                "c": [5, 5, 5, 5, 5]  # ���������
            })
        }

        # ��� ��� request.forms
        self.mock_request = MagicMock()
        
    def test_successful_prediction_simple(self):
        """���� ��������� ������������ ��� �������� ��������� ������"""
        df = self.datasets["simple_linear"]
        
        # ����������� ��� ��� request.forms
        self.mock_request.forms.get.side_effect = [
            '2',  # target_col (������ ������� - 'target')
            '6'    # features (���� ��������)
        ]
        
        # ��������� ���������� request �� ��� ���
        import sys
        sys.modules['bottle'].request = self.mock_request
        
        result = build_prediction_numbers(df)
        
        self.assertIn("��������� ������������", result)
        self.assertIn("������� ����������: target", result)
        self.assertIn("�������������� ��������", result)
        self.assertNotIn("������", result)

    def test_successful_prediction_multi_feature(self):
        """���� ��������� ������������ ��� ��������� ���������"""
        df = self.datasets["multi_feature"]
        
        self.mock_request.forms.get.side_effect = [
            '3',  # target_col (������ ������� - 'y')
            '6 1' # features (��� ��������)
        ]
        
        import sys
        sys.modules['bottle'].request = self.mock_request
        
        result = build_prediction_numbers(df)
        
        self.assertIn("x1: 6.00", result)
        self.assertIn("x2: 1.00", result)
        self.assertIn("y", result)

    def test_invalid_target_column(self):
        """���� ��������� ��������� ������ �������� �������"""
        df = self.datasets["simple_linear"]
        
        self.mock_request.forms.get.side_effect = [
            '10',  # �������������� �������
            '5'
        ]
        
        import sys
        sys.modules['bottle'].request = self.mock_request
        
        result = build_prediction_numbers(df)
        
        self.assertIn("������", result)
        self.assertIn("������������ ����� �������� �������", result)

    def test_wrong_features_count(self):
        """���� ��������� ��������� ���������� ���������"""
        df = self.datasets["multi_feature"]
        
        self.mock_request.forms.get.side_effect = [
            '3',
            '6'  # ������ ���� 2 ��������
        ]
        
        import sys
        sys.modules['bottle'].request = self.mock_request
        
        result = build_prediction_numbers(df)
        
        self.assertIn("��������� 2 ���������", result)
        self.assertIn("������", result)

    def test_non_numeric_features(self):
        """���� ��������� ���������� �������� ���������"""
        df = self.datasets["simple_linear"]
        
        self.mock_request.forms.get.side_effect = [
            '2',
            'abc'  # �� �����
        ]
        
        import sys
        sys.modules['bottle'].request = self.mock_request
        
        result = build_prediction_numbers(df)
        
        self.assertIn("������", result)
        self.assertIn("could not convert string to float", result)

    def test_constant_target_prediction(self):
        """���� ������������ ��� ����������� ������� ����������"""
        df = self.datasets["constant_target"]
        
        self.mock_request.forms.get.side_effect = [
            '3',  # target_col (������� 'c')
            '10 20'  # features (��� ��������)
        ]
        
        import sys
        sys.modules['bottle'].request = self.mock_request
        
        result = build_prediction_numbers(df)
        
        self.assertIn("�������������� ��������: 5.0000", result)
