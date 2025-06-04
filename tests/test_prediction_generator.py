import unittest
from unittest.mock import patch, mock_open
import pandas as pd

from generators import prediction_generator as pg

class TestPredictionGenerator(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'f1': [1, 2, 3, 4],
            'f2': [2, 3, 4, 5],
            'target': [3, 5, 7, 9]
        })

    def test_build_prediction_numbers_with_request(self):
        with patch.object(pg, 'request') as mock_request:
            mock_request.forms.get.side_effect = lambda k: {'target_col': '3', 'features': '5 6'}[k]
            html = pg.build_prediction_numbers(self.df)
            self.assertIn('Прогнозируемое значение', html)
            self.assertIn('target', html)
            self.assertIn('5.00', html)
            self.assertIn('6.00', html)

    def test_build_prediction_numbers_valid(self):
        html = pg.build_prediction_numbers_(self.df, 2, [5.0, 6.0])
        self.assertIn('Прогнозируемое значение', html)
        self.assertIn('target', html)

    def test_build_prediction_numbers_invalid_target(self):
        html = pg.build_prediction_numbers_(self.df, 5, [1, 2])
        self.assertIn('Ошибка', html)

    def test_build_prediction_numbers_feature_mismatch(self):
        html = pg.build_prediction_numbers_(self.df, 2, [1])
        self.assertIn('Ошибка', html)

    @patch('generators.prediction_generator.os.makedirs')
    @patch('generators.prediction_generator.open', new_callable=mock_open)
    def test_save_data_with_prediction(self, mock_file, mock_makedirs):
        with patch.object(self.df, 'to_csv') as mock_to_csv:
            pg.save_data_with_prediction(self.df, 'result')
            mock_makedirs.assert_called_once_with('data/variant4', exist_ok=True)
            mock_to_csv.assert_called_once()
            mock_file.assert_called_once()
            mock_file().write.assert_called_once_with('result')

if __name__ == '__main__':
    unittest.main()
