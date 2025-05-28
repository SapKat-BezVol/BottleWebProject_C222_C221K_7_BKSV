from __future__ import annotations

import base64
import io
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


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
