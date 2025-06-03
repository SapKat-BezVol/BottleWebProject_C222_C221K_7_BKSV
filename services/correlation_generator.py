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
    """Возвращает HTML таблицу с корреляционной матрицей."""
    corr_matrix = df.corr(numeric_only=True)
    # Округляем для удобства отображения
    corr_rounded = corr_matrix.round(2)
    # Сгенерировать HTML с видимыми границами таблицы
    html_table = corr_rounded.to_html(classes="table table-bordered table-striped", border=1)
    return f"<h3 class='mt-3'>Correlation Matrix</h3>{html_table}"


def _fig_to_base64(fig: plt.Figure) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")


def build_correlation_heatmap(df: pd.DataFrame) -> str:
    """Возвращает HTML с изображением тепловой карты корреляций в base64."""
    corr_matrix = df.corr(numeric_only=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    plt.title("Correlation Heatmap")
    b64 = _fig_to_base64(fig)
    plt.close(fig)

    return (
        "<h3 class='mt-3'>Correlation Heatmap</h3>"
        f"<img class='img-fluid' src='data:image/png;base64,{b64}' alt='heatmap'>"
    )


def analyze_correlations(df: pd.DataFrame) -> str:
    """
    Возвращает HTML с автоматическими выводами по корреляционной матрице.
    Выделяет пары с сильной положительной, сильной отрицательной и слабой корреляцией.
    """
    corr = df.corr(numeric_only=True)
    high_corr_pairs = []
    negative_corr_pairs = []
    low_corr_pairs = []

    for i in range(len(corr.columns)):
        for j in range(i + 1, len(corr.columns)):
            a, b = corr.columns[i], corr.columns[j]
            val = corr.iloc[i, j]

            if abs(val) > 0.8:
                high_corr_pairs.append((a, b, val))
            elif val < -0.5:
                negative_corr_pairs.append((a, b, val))
            elif abs(val) < 0.2:
                low_corr_pairs.append((a, b, val))

    html = """
    <div class="mt-4">
      <h4>Выводы по корреляции</h4>
      <div class="list-group">
    """

    if high_corr_pairs:
        html += """
        <div class="list-group-item list-group-item-success">
          <h6>Сильная положительная корреляция:</h6><ul class="mb-0">
        """
        for a, b, val in high_corr_pairs:
            html += f"<li> <strong>{a}</strong> и <strong>{b}</strong>: r = {val:.2f}</li>"
        html += "</ul></div>"

    if negative_corr_pairs:
        html += """
        <div class="list-group-item list-group-item-danger">
          <h6>Сильная отрицательная корреляция:</h6><ul class="mb-0">
        """
        for a, b, val in negative_corr_pairs:
            html += f"<li> <strong>{a}</strong> и <strong>{b}</strong>: r = {val:.2f}</li>"
        html += "</ul></div>"

    if low_corr_pairs:
        html += """
        <div class="list-group-item list-group-item-warning">
          <h6>Слабая или отсутствующая корреляция:</h6><ul class="mb-0">
        """
        for a, b, val in low_corr_pairs[:5]:  # максимум 5 пар
            html += f"<li> <strong>{a}</strong> и <strong>{b}</strong>: r = {val:.2f}</li>"
        html += "</ul></div>"

    if not (high_corr_pairs or negative_corr_pairs or low_corr_pairs):
        html += """
        <div class="list-group-item list-group-item-secondary">
          <em>Значимых корреляций не обнаружено.</em>
        </div>
        """

    html += "</div></div>"
    return html

def save_correlation_report(html: str, output_dir: str = "data/variant2") -> str:
    """Сохраняет HTML-отчёт и возвращает путь к файлу."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"correlation_report_{timestamp}.html"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    return filepath


def build_correlation_html(df: pd.DataFrame) -> str:
    """Генерирует полный HTML с таблицей, тепловой картой и выводами."""
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

