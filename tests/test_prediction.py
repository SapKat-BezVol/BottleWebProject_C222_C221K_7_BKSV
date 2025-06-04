import unittest
from unittest.mock import patch, mock_open
import pandas as pd

from generators import prediction_generator as pg
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
        """
        Проверяет успешное выполнение функции build_prediction.
        Ожидается:
        - возвращён HTML,
        - ошибки нет (None).
        """
        mock_build.return_value = '<div>ok</div>'
        html, err = ps.build_prediction(self.df)
        self.assertEqual(html, '<div>ok</div>')
        self.assertIsNone(err)
        mock_build.assert_called_once_with(self.df)


    @patch('services.prediction_service.build_prediction_numbers')
    def test_build_prediction_error(self, mock_build):
        """
        Проверяет поведение build_prediction при возникновении исключения.
        Ожидается:
        - HTML пустой,
        - возвращено сообщение об ошибке с классом alert-danger.
        """
        mock_build.side_effect = Exception('fail')
        html, err = ps.build_prediction(self.df)
        self.assertEqual(html, '')
        self.assertIn('alert-danger', err)


    @patch('services.prediction_service.save_data_with_prediction')
    @patch('services.prediction_service.build_prediction_numbers_')
    def test_save_prediction(self, mock_build, mock_save):
        """
        Проверяет сохранение результата прогнозирования.
        Ожидается:
        - вызов build_prediction_numbers_ с правильными аргументами,
        - вызов save_data_with_prediction с результатом,
        - возвращено сообщение об успешном сохранении.
        """
        mock_build.return_value = 'result'
        msg = ps.save_prediction(self.df, 2, [1.0, 2.0])
        mock_build.assert_called_once_with(self.df, 2, [1.0, 2.0])
        mock_save.assert_called_once_with(self.df, 'result')
        self.assertIn('успешно', msg)


class TestPredictionGenerator(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'f1': [1, 2, 3, 4],
            'f2': [2, 3, 4, 5],
            'target': [3, 5, 7, 9]
        })


    def test_build_prediction_numbers_with_request(self):
        """
        Проверяет работу функции build_prediction_numbers с имитацией HTTP-запроса.
        Ожидается:
        - корректная обработка формы,
        - вывод значений признаков и целевой переменной в HTML.
        """
        with patch.object(pg, 'request') as mock_request:
            mock_request.forms.get.side_effect = lambda k: {'target_col': '3', 'features': '5 6'}[k]
            html = pg.build_prediction_numbers(self.df)
            self.assertIn('Прогнозируемое значение', html)
            self.assertIn('target', html)
            self.assertIn('5.00', html)
            self.assertIn('6.00', html)


    def test_build_prediction_numbers_valid(self):
        """
        Проверяет работу функции build_prediction_numbers_ с корректными данными.
        Ожидается:
        - наличие ключевых строк в HTML-результате.
        """
        html = pg.build_prediction_numbers_(self.df, 2, [5.0, 6.0])
        self.assertIn('Прогнозируемое значение', html)
        self.assertIn('target', html)


    def test_build_prediction_numbers_invalid_target(self):
        """
        Проверяет обработку ошибки при запросе большего числа прогнозов, чем доступно данных.
        Ожидается:
        - появление сообщения об ошибке в HTML.
        """
        html = pg.build_prediction_numbers_(self.df, 5, [1, 2])
        self.assertIn('Ошибка', html)


    def test_build_prediction_numbers_feature_mismatch(self):
        """
        Проверяет обработку ошибки при неверном количестве входных признаков.
        Ожидается:
        - появление сообщения об ошибке в HTML.
        """
        html = pg.build_prediction_numbers_(self.df, 2, [1])
        self.assertIn('Ошибка', html)


    @patch('generators.prediction_generator.os.makedirs')
    @patch('generators.prediction_generator.open', new_callable=mock_open)
    def test_save_data_with_prediction(self, mock_file, mock_makedirs):
        """
        Проверяет корректность сохранения данных и результата прогноза в файл.
        Ожидается:
        - создание директории data/variant4,
        - запись CSV-файла и текстового результата.
        """
        with patch.object(self.df, 'to_csv') as mock_to_csv:
            pg.save_data_with_prediction(self.df, 'result')
            mock_makedirs.assert_called_once_with('data/variant4', exist_ok=True)
            mock_to_csv.assert_called_once()
            mock_file.assert_called_once()
            mock_file().write.assert_called_once_with('result')


if __name__ == '__main__':
    unittest.main()