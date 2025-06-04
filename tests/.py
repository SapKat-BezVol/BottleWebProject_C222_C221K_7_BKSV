import unittest
from unittest.mock import patch
import pandas as pd

import services.prediction_service as ps

class TestPredictionService(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'f1': [1, 2],
            'f2': [2, 3],
            'target': [3, 5]
        })
    @patch('services.prediction_service.build_prediction_numbers')
    def test_build_prediction_success(self, mock_build):
        mock_build.return_value = '<div>ok</div>'
        html, err = ps.build_prediction(self.df)
        self.assertEqual(html, '<div>ok</div>')
        self.assertIsNone(err)
        mock_build.assert_called_once_with(self.df)

    @patch('services.prediction_service.build_prediction_numbers')
    def test_build_prediction_error(self, mock_build):
        mock_build.side_effect = Exception('fail')
        html, err = ps.build_prediction(self.df)
        self.assertEqual(html, '')
        self.assertIn('alert-danger', err)

    @patch('services.prediction_service.save_data_with_prediction')
    @patch('services.prediction_service.build_prediction_numbers_')
    def test_save_prediction(self, mock_build, mock_save):
        mock_build.return_value = 'result'
        msg = ps.save_prediction(self.df, 2, [1.0, 2.0])
        mock_build.assert_called_once_with(self.df, 2, [1.0, 2.0])
        mock_save.assert_called_once_with(self.df, 'result')
        self.assertIn('успешно', msg)

if __name__ == '__main__':
    unittest.main()
