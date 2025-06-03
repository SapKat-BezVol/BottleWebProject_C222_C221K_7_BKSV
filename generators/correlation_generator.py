from __future__ import annotations

import base64
import io
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

def build_correlation_table(df: pd.DataFrame) -> str:
    """Создаёт HTML-таблицу с корреляционной матрицей на основе числовых данных."""
    corr_matrix = df.corr(numeric_only=True)        # Вычисляем корреляционную матрицу только по числовым столбцам
    corr_rounded = corr_matrix.round(2)             # Округляем значения до 2 знаков после запятой
    html_table = corr_rounded.to_html(              # Преобразуем DataFrame в HTML-таблицу
        classes="table table-bordered table-striped", border=1
    )
    return f"<h3 class='mt-3'>Correlation Matrix</h3>{html_table}"  # Добавляем заголовок


def _fig_to_base64(fig: plt.Figure) -> str:
    """Преобразует matplotlib-график в base64-строку для вставки в HTML."""
    buf = io.BytesIO()                              # Создаём буфер в памяти
    fig.savefig(buf, format="png", bbox_inches="tight")  # Сохраняем график в буфер
    buf.seek(0)                                      # Перемещаемся в начало буфера
    return base64.b64encode(buf.read()).decode("ascii")  # Кодируем в base64



def build_correlation_heatmap(df: pd.DataFrame) -> str:
    """Генерирует тепловую карту корреляций и возвращает HTML-изображение."""
    corr_matrix = df.corr(numeric_only=True)         # Корреляции между числовыми столбцами
    fig, ax = plt.subplots(figsize=(8, 6))            # Создаём график
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)  # Тепловая карта
    plt.title("Correlation Heatmap")
    b64 = _fig_to_base64(fig)                         # Преобразуем график в base64
    plt.close(fig)                                    # Закрываем фигуру (освобождаем память)

    return (
        "<h3 class='mt-3'>Correlation Heatmap</h3>"
        f"<img class='img-fluid' src='data:image/png;base64,{b64}' alt='heatmap'>"
    )



def analyze_correlations(df: pd.DataFrame) -> str:
    """
    Проводит анализ значений корреляции и выделяет:
    - Сильную положительную (> 0.8)
    - Сильную отрицательную (< -0.5)
    - Слабую (< 0.2)
    """
    corr = df.corr(numeric_only=True)
    high_corr_pairs, negative_corr_pairs, low_corr_pairs = [], [], []

    # Проходим по всем уникальным парам
    for i in range(len(corr.columns)):
        for j in range(i + 1, len(corr.columns)):
            a, b = corr.columns[i], corr.columns[j]
            val = corr.iloc[i, j]
            if val < -0.5:
                negative_corr_pairs.append((a, b, val))
            elif val > 0.8:
                high_corr_pairs.append((a, b, val))
            elif abs(val) < 0.2:
                low_corr_pairs.append((a, b, val))

    # Формируем HTML-блоки
    html = """
    <div class="mt-4">
      <h4>Выводы по корреляции</h4>
      <div class="list-group">
    """

    # Добавляем списки в зависимости от наличия корреляций
    if high_corr_pairs:
        html += "<div class='list-group-item list-group-item-success'><h6>Сильная положительная корреляция:</h6><ul class='mb-0'>"
        for a, b, val in high_corr_pairs:
            html += f"<li><strong>{a}</strong> и <strong>{b}</strong>: r = {val:.2f}</li>"
        html += "</ul></div>"

    if negative_corr_pairs:
        html += "<div class='list-group-item list-group-item-danger'><h6>Сильная отрицательная корреляция:</h6><ul class='mb-0'>"
        for a, b, val in negative_corr_pairs:
            html += f"<li><strong>{a}</strong> и <strong>{b}</strong>: r = {val:.2f}</li>"
        html += "</ul></div>"

    if low_corr_pairs:
        html += "<div class='list-group-item list-group-item-warning'><h6>Слабая или отсутствующая корреляция:</h6><ul class='mb-0'>"
        for a, b, val in low_corr_pairs[:5]:  # максимум 5
            html += f"<li><strong>{a}</strong> и <strong>{b}</strong>: r = {val:.2f}</li>"
        html += "</ul></div>"

    if not (high_corr_pairs or negative_corr_pairs or low_corr_pairs):
        html += "<div class='list-group-item list-group-item-secondary'><em>Значимых корреляций не обнаружено.</em></div>"

    html += "</div></div>"
    return html


def save_correlation_report(html: str, output_dir: str = "data/variant2") -> str:
    """Сохраняет HTML-отчёт в файл с уникальным именем."""
    os.makedirs(output_dir, exist_ok=True)                           # Создаём папку, если не существует
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")             # Текущая дата и время
    filename = f"correlation_report_{timestamp}.html"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)                                                # Сохраняем HTML в файл

    return filepath



def build_correlation_html(df: pd.DataFrame) -> str:
    """Объединяет таблицу, тепловую карту и выводы в единый HTML-отчёт."""
    table_html = build_correlation_table(df)
    heatmap_html = build_correlation_heatmap(df)
    analysis_html = analyze_correlations(df)

    return f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Correlation Report</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{ padding: 2rem; font-family: sans-serif; }}
                h2, h3, h4 {{ margin-top: 2rem; }}
                img {{ max-width: 100%; height: auto; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2 class="mb-4">Correlation Analysis Report</h2>
                {table_html}
                <hr class="my-4">
                {heatmap_html}
                <hr class="my-4">
                {analysis_html}
            </div>
        </body>
        </html>
    """

