# Импорт будущих возможностей Python
from __future__ import annotations

# Импорт стандартных библиотек
import base64
import io
from typing import List, Tuple

# Импорт и настройка библиотеки matplotlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Импорт pandas и метода для построения scatter matrix
import pandas as pd
from pandas.plotting import scatter_matrix

# Указываем, какие функции экспортируются из модуля
__all__ = [
    "build_plot_html",
]

# Вспомогательная функция: преобразует объект Figure в строку base64
def _fig_to_base64(fig: plt.Figure) -> str:
    """Преобразует matplotlib-фигуру *fig* в base64-кодированное PNG-изображение,
    подходящее для использования в атрибуте <img src="">."""
    buf = io.BytesIO()  # создаем буфер в памяти
    fig.savefig(buf, format="png", bbox_inches="tight")  # сохраняем фигуру в буфер в формате PNG
    buf.seek(0)  # перемещаем указатель в начало
    return base64.b64encode(buf.read()).decode("ascii")  # кодируем содержимое в base64 и возвращаем строку

# Построение гистограмм для каждого числового столбца
def _build_histograms(df: pd.DataFrame) -> List[Tuple[str, str]]:
    """Строит гистограмму для каждого числового столбца датафрейма."""
    images: List[Tuple[str, str]] = []
    numeric = df.select_dtypes(include="number")  # выбираем только числовые столбцы
    if numeric.empty:
        raise ValueError("Нет числовых столбцов для гистограмм.")
    for col in numeric.columns:
        fig = plt.figure(figsize=(6, 4))
        numeric[col].hist(bins=15)  # создаем гистограмму
        plt.title(f"Histogram of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        images.append((col, _fig_to_base64(fig)))  # сохраняем base64-картинку
        plt.close(fig)  # закрываем фигуру для освобождения памяти
    return images

# Построение box-plot для каждого числового столбца
def _build_boxplots(df: pd.DataFrame) -> List[Tuple[str, str]]:
    """Строит box-plot (ящик с усами) для каждого числового столбца датафрейма."""
    images: List[Tuple[str, str]] = []
    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        raise ValueError("Нет числовых столбцов для box-plots.")
    for col in numeric.columns:
        fig = plt.figure(figsize=(6, 4))
        numeric[col].plot.box(vert=True)  # box-plot вертикально
        plt.title(f"Boxplot of {col}")
        images.append((col, _fig_to_base64(fig)))  # сохраняем картинку
        plt.close(fig)
    return images

# Построение scatter matrix — матрицы диаграмм рассеяния
def _build_scatter_matrix(df: pd.DataFrame) -> List[Tuple[str, str]]:
    """Строит scatter matrix (матрицу диаграмм рассеяния) по числовым столбцам."""
    numeric = df.select_dtypes(include="number")
    if numeric.shape[1] < 2:
        raise ValueError("Для scatter matrix нужно минимум 2 числовых столбца.")
    axes = scatter_matrix(numeric, figsize=(8, 8), diagonal="hist")  # создаем матрицу рассеяния
    fig = axes[0, 0].get_figure()  # получаем общую фигуру
    b64 = _fig_to_base64(fig)  # кодируем изображение
    plt.close(fig)
    return [("scatter_matrix", b64)]  # возвращаем список с одной картинкой

# Основная функция: создает HTML с графиками по типу
def build_plot_html(df: pd.DataFrame, plot_type: str) -> str:
    """
    Возвращает HTML-фрагмент с изображениями заданного типа:
      - "hist"    → гистограммы для каждого числового столбца
      - "box"     → box-plots для каждого числового столбца
      - "scatter" → scatter matrix для всех числовых столбцов
    """
    # Сопоставляем тип графика с соответствующей функцией построения и заголовком
    builders = {
        "hist": (_build_histograms, "Гистограммы"),
        "box": (_build_boxplots, "Box-plots"),
        "scatter": (_build_scatter_matrix, "Scatter Matrix"),
    }

    if plot_type not in builders:
        raise ValueError(f"Неизвестный plot_type: {plot_type!r}")

    build_func, title = builders[plot_type]  # получаем соответствующую функцию и заголовок
    images = build_func(df)

    # Формируем HTML: сначала заголовок, потом каждое изображение с подзаголовком
    html_parts: List[str] = [f"<h3 class='mt-3'>{title}</h3>"]
    for label, b64 in images:
        display_label = label if plot_type != "scatter" else ""  # scatter не имеет подзаголовков
        if display_label:
            html_parts.append(f"<h4>{display_label}</h4>")
        html_parts.append(
            f"<img class='img-fluid mb-3' "
            f"src='data:image/png;base64,{b64}' "
            f"alt='{display_label or title}'>"
        )

    return "\n".join(html_parts)
