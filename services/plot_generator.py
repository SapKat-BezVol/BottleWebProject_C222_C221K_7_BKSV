from __future__ import annotations

import base64
import io
from typing import List, Tuple
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import scatter_matrix

__all__ = [
    "build_plot_html",
]

def _fig_to_base64(fig: plt.Figure) -> str:
    """Convert *fig* to base64-encoded PNG suitable for an <img> *src* attribute."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")


def _build_histograms(df: pd.DataFrame) -> List[Tuple[str, str]]:
    """Histogram for every numeric column."""
    images: List[Tuple[str, str]] = []
    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        raise ValueError("Нет числовых столбцов для гистограмм.")
    for col in numeric.columns:
        fig = plt.figure(figsize=(6, 4))
        numeric[col].hist(bins=15)
        plt.title(f"Histogram of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        images.append((col, _fig_to_base64(fig)))
        plt.close(fig)
    return images


def _build_boxplots(df: pd.DataFrame) -> List[Tuple[str, str]]:
    """Box-plot for every numeric column."""
    images: List[Tuple[str, str]] = []
    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        raise ValueError("Нет числовых столбцов для box-plots.")
    for col in numeric.columns:
        fig = plt.figure(figsize=(6, 4))
        numeric[col].plot.box(vert=True)
        plt.title(f"Boxplot of {col}")
        images.append((col, _fig_to_base64(fig)))
        plt.close(fig)
    return images


def _build_scatter_matrix(df: pd.DataFrame) -> List[Tuple[str, str]]:
    """Scatter matrix over all numeric columns (единственная картинка)."""
    numeric = df.select_dtypes(include="number")
    if numeric.shape[1] < 2:
        raise ValueError("Для scatter matrix нужно минимум 2 числовых столбца.")
    axes = scatter_matrix(numeric, figsize=(8, 8), diagonal="hist")
    fig = axes[0, 0].get_figure()
    b64 = _fig_to_base64(fig)
    plt.close(fig)
    return [("scatter_matrix", b64)]


def build_plot_html(df: pd.DataFrame, plot_type: str) -> str:
    """
    Возвращает HTML-фрагмент с картинками выбранного типа:
      - "hist"    → гистограммы по каждому числовому столбцу
      - "box"     → box-plots по каждому числовому столбцу
      - "scatter" → scatter matrix для числовых столбцов
    """
    builders = {
        "hist": (_build_histograms, "Гистограммы"),
        "box": (_build_boxplots, "Box-plots"),
        "scatter": (_build_scatter_matrix, "Scatter Matrix"),
    }
    if plot_type not in builders:
        raise ValueError(f"Неизвестный plot_type: {plot_type!r}")
    build_func, title = builders[plot_type]
    images = build_func(df)

    html_parts: List[str] = [f"<h3 class='mt-3'>{title}</h3>"]
    for label, b64 in images:
        display_label = label if plot_type != "scatter" else ""
        if display_label:
            html_parts.append(f"<h4>{display_label}</h4>")
        html_parts.append(
            f"<img class='img-fluid mb-3' "
            f"src='data:image/png;base64,{b64}' "
            f"alt='{display_label or title}'>"
        )

    return "\n".join(html_parts)
