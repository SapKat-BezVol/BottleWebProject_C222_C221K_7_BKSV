import unittest
from unittest.mock import patch, MagicMock, call
import pandas as pd
import numpy as np
import base64
import io
import os

# Импорт тестируемых функций
from generators.plot_generator import (
    build_plot_html,
    _fig_to_base64,
    _save_html_file,
    _basic_hist_stats,
    _hist_stats_table,
    _box_stats_table,
    _build_histograms,
    _build_boxplots,
    _build_scatter_matrix,
    _HIST_DESCRIPTIONS
)

# Настройка неинтерактивного бэкенда Matplotlib для тестов
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class TestPlotGenerator(unittest.TestCase):
    """
    Класс для модульного тестирования функций генерации графиков и HTML из модуля plot_generator.

    Содержит тесты на корректность вычислений статистик, генерацию и сохранение графиков, 
    а также формирование HTML-таблиц и страниц.
    """

    def setUp(self):
        """
        Подготовка тестовых DataFrame и Series для использования в тестах.
        """
        self.df_numeric = pd.DataFrame({
            'ColA': np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
            'ColB': np.array([5.0, 4.0, 3.0, 2.0, 1.0]),
            'ColC': np.array([1.0, 1.0, 2.0, 2.0, 3.0])
        })
        self.df_mixed = pd.DataFrame({
            'Num1': [1, 2, 3, 4, 5],
            'Cat1': ['a', 'b', 'c', 'd', 'e'],
            'Num2': [0.1, 0.2, 0.3, 0.4, 0.5]
        })
        self.df_non_numeric = pd.DataFrame({
            'TextA': ['apple', 'banana', 'cherry'],
            'TextB': ['dog', 'cat', 'mouse']
        })
        self.df_one_numeric = pd.DataFrame({
            'SingleNum': [10, 20, 30],
            'Text': ['x', 'y', 'z']
        })
        self.df_two_numeric = pd.DataFrame({
            'NumX': [1, 2, 3],
            'NumY': [4, 5, 6]
        })
        self.sample_series = pd.Series([1, 2, 2, 3, 3, 3, 4, 4, 5, np.nan])

    def test_fig_to_base64(self):
        """
        Проверка конвертации объекта Figure Matplotlib в строку base64.
        """
        fig = plt.figure()
        plt.plot([1, 2, 3])
        base64_str = _fig_to_base64(fig)
        plt.close(fig)
        self.assertIsInstance(base64_str, str)
        self.assertTrue(len(base64_str) > 0)
        try:
            base64.b64decode(base64_str)
        except Exception:
            self.fail("_fig_to_base64 не вернул валидную строку base64.")

    @patch('generators.plot_generator.os.makedirs')
    @patch('generators.plot_generator.open', new_callable=unittest.mock.mock_open)
    @patch('generators.plot_generator.uuid.uuid4')
    def test_save_html_file(self, mock_uuid, mock_open_file, mock_makedirs):
        """
        Проверка сохранения HTML-файла с уникальным именем и созданием директории.
        """
        mock_uuid.return_value.hex = "testuuid"
        content = "<html><body>Test</body></html>"
        base_name = "test_plot"

        _save_html_file(content, base_name)

        mock_makedirs.assert_called_once_with("data/variant3", exist_ok=True)
        expected_filepath = os.path.join("data/variant3", f"{base_name}_testuuid.html")
        mock_open_file.assert_called_once_with(expected_filepath, "w", encoding="utf-8")
        mock_open_file().write.assert_called_once_with(content)

    def test_basic_hist_stats(self):
        """
        Проверка расчёта базовых статистик для Series.
        """
        stats = _basic_hist_stats(self.sample_series)
        self.assertEqual(stats['count'], 9)
        self.assertAlmostEqual(stats['mean'], self.sample_series.mean())
        self.assertAlmostEqual(stats['median'], self.sample_series.median())
        self.assertAlmostEqual(stats['std'], self.sample_series.std())
        self.assertAlmostEqual(stats['min'], 1.0)
        self.assertAlmostEqual(stats['max'], 5.0)

    def test_hist_stats_table(self):
        """
        Проверка генерации HTML-таблицы для статистик гистограммы.
        """
        stats = {'count': 10, 'mean': 5.5, 'median': 5.0, 'unknown_stat': 'value'}
        html = _hist_stats_table(stats)
        self.assertIn("<tr><td>count</td><td>Количество наблюдений</td><td>10.0000</td></tr>", html)
        self.assertIn("<tr><td>mean</td><td>Среднее арифметическое</td><td>5.5000</td></tr>", html)
        self.assertIn("<tr><td>median</td><td>Медиана (50‑й перцентиль)</td><td>5.0000</td></tr>", html)
        # Проверка fallback-описания
        self.assertIn("<tr><td>unknown_stat</td><td>unknown_stat</td><td>value</td></tr>", html)
        self.assertTrue(html.startswith("<table class='table table-bordered table-sm'>"))
        self.assertTrue(html.endswith("</tbody></table>"))

    def test_box_stats_table(self):
        """
        Проверка генерации HTML-таблицы статистик для box-plot.
        """
        stats = {
            'ColA': {'min': 1, 'q1': 2, 'median': 3, 'q3': 4, 'max': 5, 'iqr': 2, 'outliers_percent': 0.0},
            'ColB': {'min': 0.1, 'q1': 0.2, 'median': 0.3, 'q3': 0.4, 'max': 0.5, 'iqr': 0.2, 'outliers_percent': 10.55}
        }
        html = _box_stats_table(stats)
        self.assertIn("<th>Столбец</th>", html)
        self.assertIn("<td>ColA</td><td>1.0000</td>", html)
        self.assertIn("<td>0.00</td></tr>", html)
        self.assertIn("<td>ColB</td><td>0.1000</td>", html)
        self.assertIn("<td>10.55</td></tr>", html)
        self.assertTrue(html.startswith("<table class='table table-bordered table-sm table-scroll'>"))

    @patch('generators.plot_generator._save_html_file')
    def test_build_histograms(self, mock_save_html):
        """
        Проверка генерации гистограмм для числовых столбцов DataFrame.
        Проверяется формирование результата, содержимое и обработка нечисловых данных.
        """
        results = _build_histograms(self.df_numeric)
        self.assertEqual(len(results), 3)
        for col_name, img64, stats_html in results:
            self.assertIn(col_name, ['ColA', 'ColB', 'ColC'])
            self.assertTrue(img64.startswith("iVBORw0KGgo"))
            self.assertIn(f"<td>{_HIST_DESCRIPTIONS['mean']}</td>", stats_html)
        self.assertEqual(mock_save_html.call_count, 3)
        mock_save_html.assert_any_call(unittest.mock.ANY, "histogram_ColA")

        # Проверка работы с DataFrame смешанного типа
        results_mixed = _build_histograms(self.df_mixed)
        self.assertEqual(len(results_mixed), 2)
        self.assertEqual(mock_save_html.call_count, 5)

        # Проверка исключения при отсутствии числовых столбцов
        with self.assertRaisesRegex(ValueError, "Нет числовых столбцов для гистограмм."):
            _build_histograms(self.df_non_numeric)

    @patch('generators.plot_generator._save_html_file')
    def test_build_boxplots(self, mock_save_html):
        """
        Проверка генерации box-plot для числовых столбцов.
        """
        results = _build_boxplots(self.df_numeric)
        self.assertEqual(len(results), 1)
        label, img64, stats_html = results[0]
        self.assertEqual(label, "Box-plot")
        self.assertTrue(img64.startswith("iVBORw0KGgo"))
        self.assertIn("<th>Столбец</th><th>Минимум</th>", stats_html)
        self.assertIn("<td>ColA</td>", stats_html)
        self.assertIn("<td>ColB</td>", stats_html)
        self.assertIn("<td>ColC</td>", stats_html)
        mock_save_html.assert_called_once()
        mock_save_html.assert_called_with(unittest.mock.ANY, "boxplot_all_columns")

        # Проверка исключения при отсутствии числовых столбцов
        with self.assertRaisesRegex(ValueError, "Нет числовых столбцов для box‑plot."):
            _build_boxplots(self.df_non_numeric)

    @patch('generators.plot_generator._save_html_file')
    def test_build_scatter_matrix(self, mock_save_html):
        """
        Проверка генерации scatter-matrix для DataFrame с минимум двумя числовыми столбцами.
        """
        results = _build_scatter_matrix(self.df_numeric)
        self.assertEqual(len(results), 1)
        label, img64, stats_html = results[0]
        self.assertEqual(label, "Scatter-matrix")
        self.assertTrue(img64.startswith("iVBORw0KGgo"))
        self.assertEqual(stats_html, "")
        mock_save_html.assert_called_once()
        mock_save_html.assert_called_with(unittest.mock.ANY, "scatter_matrix")

        # Проверка исключения при недостаточном числе числовых столбцов
        with self.assertRaisesRegex(ValueError, "Для scatter‑matrix нужно минимум два числовых столбца."):
            _build_scatter_matrix(self.df_one_numeric)
        with self.assertRaisesRegex(ValueError, "Для scatter‑matrix нужно минимум два числовых столбца."):
            _build_scatter_matrix(self.df_non_numeric)

    @patch('generators.plot_generator._save_html_file')
    def test_build_plot_html_hist(self, mock_save_html):
        """
        Проверка генерации итоговой HTML-страницы для гистограмм.
        """
        html_output = build_plot_html(self.df_numeric, "hist")
        self.assertIn("<h3 class='mt-3 mb-4'>Гистограммы</h3>", html_output)
        self.assertEqual(html_output.count("<div class='card mb-4'>"), 3)
        self.assertIn("alt='ColA'", html_output)
        self.assertIn("alt='ColB'", html_output)
        self.assertIn("alt='ColC'", html_output)
        self.assertIn("src='data:image/png;base64,", html_output)
        self.assertIn("Количество наблюдений", html_output)
        self.assertEqual(mock_save_html.call_count, 3)

    @patch('generators.plot_generator._save_html_file')
    def test_build_plot_html_box(self, mock_save_html):
        """
        Проверка генерации итоговой HTML-страницы для box-plot.
        """
        html_output = build_plot_html(self.df_numeric, "box")
        self.assertIn("<h3 class='mt-3 mb-4'>Box-plot</h3>", html_output)
        self.assertEqual(html_output.count("<div class='card mb-4'>"), 1)
        self.assertIn("alt='Box-plot'", html_output)
        self.assertIn("src='data:image/png;base64,", html_output)
        self.assertIn("<th>Столбец</th><th>Минимум</th>", html_output)
        self.assertEqual(mock_save_html.call_count, 1)

    @patch('generators.plot_generator._save_html_file')
    def test_build_plot_html_scatter(self, mock_save_html):
        """
        Проверка генерации итоговой HTML-страницы для scatter-matrix.
        """
        html_output = build_plot_html(self.df_two_numeric, "scatter")
        self.assertIn("<h3 class='mt-3 mb-4'>Scatter-matrix</h3>", html_output)
        self.assertEqual(html_output.count("<div class='card mb-4'>"), 1)
        self.assertIn("alt='Scatter-matrix'", html_output)
        self.assertIn("src='data:image/png;base64,", html_output)
        self.assertNotIn("<th>Код</th><th>Описание</th>", html_output)
        self.assertEqual(mock_save_html.call_count, 1)

    def test_build_plot_html_invalid_type(self):
        """
        Проверка выброса исключения при указании неизвестного типа графика.
        """
        with self.assertRaisesRegex(ValueError, "Неизвестный plot_type: 'invalid_plot'"):
            build_plot_html(self.df_numeric, "invalid_plot")

    def test_build_plot_html_no_numeric_data_hist(self):
        """
        Проверка выброса исключения при отсутствии числовых данных для гистограмм.
        """
        with self.assertRaisesRegex(ValueError, "Нет числовых столбцов для гистограмм."):
            build_plot_html(self.df_non_numeric, "hist")

    def test_build_plot_html_no_numeric_data_box(self):
        """
        Проверка выброса исключения при отсутствии числовых данных для box-plot.
        """
        with self.assertRaisesRegex(ValueError, "Нет числовых столбцов для box‑plot."):
            build_plot_html(self.df_non_numeric, "box")

    def test_build_plot_html_insufficient_numeric_data_scatter(self):
        """
        Проверка выброса исключения при недостаточном количестве числовых столбцов для scatter-matrix.
        """
        with self.assertRaisesRegex(ValueError, "Для scatter‑matrix нужно минимум два числовых столбца."):
            build_plot_html(self.df_one_numeric, "scatter")

    def test_build_plot_html_structure_hist(self):
        """
        Проверка структуры итогового HTML для гистограмм.
        """
        html_output = build_plot_html(self.df_one_numeric, "hist")
        self.assertIn("<div class='col-md-6 text-center'>", html_output)
        self.assertIn("<div class='col-md-6'>", html_output)
        self.assertIn("class='img-fluid d-block mx-auto'", html_output)

    def test_build_plot_html_structure_box(self):
        """
        Проверка структуры итогового HTML для box-plot.
        """
        html_output = build_plot_html(self.df_numeric, "box")
        self.assertIn("<div class='card-body text-center'>", html_output)
        self.assertIn("<img class='img-fluid d-block mx-auto'", html_output)
        self.assertIn("<div class='mt-3'>", html_output)

    def test_build_plot_html_structure_scatter(self):
        """
        Проверка структуры итогового HTML для scatter-matrix (без блока статистик в карточке).
        """
        html_output = build_plot_html(self.df_two_numeric, "scatter")
        self.assertIn("<div class='col-md-6 text-center'>", html_output)
        self.assertIn("<div class='row justify-content-center'>", html_output)
        self.assertNotIn("table-bordered", html_output)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
