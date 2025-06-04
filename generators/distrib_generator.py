from __future__ import annotations  # Позволяет использовать типы в аннотациях (например, pd.DataFrame)
import base64  
import io
import os     
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  # Построение графиков
import seaborn as sns          # Улучшенная визуализация графиков
from scipy import stats        # Статистические функции

def _fig_to_base64(fig: plt.Figure) -> str:
    """
    Преобразует график matplotlib в строку в формате base64.
    Это позволяет вставить изображение прямо в HTML-документ.
    """
    buf = io.BytesIO()               # Создаем буфер в памяти
    fig.savefig(buf, format='png', bbox_inches='tight')  # Сохраняем график как PNG
    buf.seek(0)                      # Возвращаем указатель на начало буфера
    return base64.b64encode(buf.read()).decode('ascii')  # Кодируем в base64 и возвращаем строку

def analyze_distributions(df: pd.DataFrame) -> dict:
    """
    Для каждого числового столбца рассчитывает статистики и строит гистограмму с KDE.
    Возвращает словарь, где ключ — имя столбца, значение — словарь со статистикой и изображением.
    """
    results = {}  # Хранилище результатов анализа

    # Перебираем только числовые столбцы
    for col in df.select_dtypes(include=['number']).columns:
        col_data = df[col].dropna()  # Удаляем пропуски

        if len(col_data) < 2:  # Пропускаем слишком маленькие выборки
            continue

        # Вычисляем основные статистики
        stats_dict = {
            'mean': col_data.mean(),
            'median': col_data.median(),
            'std': col_data.std(),
            'skewness': col_data.skew(),         # Асимметрия
            'kurtosis': col_data.kurtosis(),     # Эксцесс
            # Тест Шапиро-Уилка на нормальность (только если данных не больше 5000)
            'shapiro_p': stats.shapiro(col_data)[1] if len(col_data) <= 5000 else None
        }

        # Определяем, является ли распределение нормальным по тесту Шапиро
        is_normal = False
        if stats_dict['shapiro_p'] is not None:
            is_normal = stats_dict['shapiro_p'] > 0.05  # p > 0.05 → нет оснований отвергать нулевую гипотезу о нормальности

        # Добавляем признак нормальности
        stats_dict['is_normal'] = is_normal

        # Определение выбросов через межквартильный размах (IQR)
        q1 = col_data.quantile(0.25)
        q3 = col_data.quantile(0.75)
        iqr = q3 - q1
        outliers = col_data[(col_data < (q1 - 1.5 * iqr)) | (col_data > (q3 + 1.5 * iqr))]
        stats_dict['outliers_count'] = len(outliers)
        stats_dict['outliers_percent'] = len(outliers) / len(col_data) * 100

        # Строим график
        plt.figure(figsize=(10, 6))
        sns.histplot(col_data, kde=True, stat='density', label='Распределение данных')

        plt.title(f'Распределение {col}')

        # Если распределение нормальное, рисуем теоретическую кривую нормального распределения
        if is_normal:
            plt.axvline(stats_dict['mean'], color='r', linestyle='--', label='Среднее')
            x = np.linspace(col_data.min(), col_data.max(), 100)
            plt.plot(x, stats.norm.pdf(x, stats_dict['mean'], stats_dict['std']), 'r-', lw=2, label='Нормальное распределение')
            plt.legend()
        else:
            plt.legend()

        # Конвертируем график в base64
        plot_b64 = _fig_to_base64(plt.gcf())
        plt.close()  # Закрываем текущий график, чтобы не мешал следующим построениям

        # Сохраняем данные по столбцу
        results[col] = {'stats': stats_dict, 'plot': plot_b64}

    return results

def generate_distribution_html(df: pd.DataFrame) -> str:
    """
    Генерирует HTML-страницу с анализом распределений числовых столбцов.
    """
    analysis = analyze_distributions(df)

    # Если нет числовых столбцов, выводим предупреждение
    if not analysis:
        return "<div class='alert alert-warning'>Нет числовых столбцов для анализа</div>"

    html_parts = []  # Список HTML-частей для объединения в финальный документ
    for col, data in analysis.items():
        stats = data['stats']
        # Формируем HTML-карточку для каждого столбца
        stats_html = f"""
        <div class='card mb-4'>
            <div class='card-header'>
                <h4>Столбец: {col}</h4>
            </div>
            <div class='card-body'>
                <div class='row'>
                    <div class='col-md-6'>
                        <img class='img-fluid' src='data:image/png;base64,{data["plot"]}'>
                    </div>
                    <div class='col-md-6'>
                        <table class='table table-bordered'>
                            <tr><th>Характеристика</th><th>Значение</th></tr>
                            <tr><td>Среднее</td><td>{stats['mean']:.4f}</td></tr>
                            <tr><td>Медиана</td><td>{stats['median']:.4f}</td></tr>
                            <tr><td>Станд. отклонение</td><td>{stats['std']:.4f}</td></tr>
                            <tr><td>Асимметрия</td><td>{stats['skewness']:.4f}</td></tr>
                            <tr><td>Эксцесс</td><td>{stats['kurtosis']:.4f}</td></tr>
                            <tr><td>Нормальное распределение?</td>
                                <td>{'Да' if stats['is_normal'] else 'Нет'}</td></tr>
                            <tr><td>Количество выбросов</td><td>{stats['outliers_count']}</td></tr>
                            <tr><td>Процент выбросов</td><td>{stats['outliers_percent']:.2f}%</td></tr>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        """
        html_parts.append(stats_html)
    # Объединяем все карточки в один HTML-документ
    return "\n".join(html_parts)