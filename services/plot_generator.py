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


def _fig_to_base64(fig: "plt.Figure") -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")


def _build_histograms(df: pd.DataFrame) -> List[Tuple[str, str]]:
    """Histogram for every column."""
    images: List[Tuple[str, str]] = []
    for col in df.columns:
        fig = plt.figure()
        df[col].hist()
        plt.title(f"Histogram of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        images.append((col, _fig_to_base64(fig)))
        plt.close(fig)
    return images


def _build_boxplots(df: pd.DataFrame) -> List[Tuple[str, str]]:
    """Box-plot for every column."""
    images: List[Tuple[str, str]] = []
    for col in df.columns:
        fig = plt.figure()
        df.boxplot(column=col)
        plt.title(f"Box-plot of {col}")
        images.append((col, _fig_to_base64(fig)))
        plt.close(fig)
    return images


def _build_scatter_matrix(df: pd.DataFrame) -> str:
    """Full scatter-matrix for *df*. Returns a single base64 image."""
    # pandas returns an array of Axes; any of them carries the underlying Figure.
    axes = scatter_matrix(df, diagonal="hist", figsize=(8, 8))
    fig = axes[0][0].get_figure()
    b64 = _fig_to_base64(fig)
    plt.close(fig)
    return b64


def build_plot_html(plot_type: str, df: pd.DataFrame) -> str:
    plot_type = (plot_type or "hist").lower()

    if plot_type == "hist":
        title = "Гистограммы"
        imgs = _build_histograms(df)
    elif plot_type == "box":
        title = "Box-plots"
        imgs = _build_boxplots(df)
    elif plot_type == "scatter":
        b64 = _build_scatter_matrix(df)
        return (
            "<h3 class='mt-3'>Scatter matrix</h3>"
            f"<img class='img-fluid' src='data:image/png;base64,{b64}' alt='scatter-matrix'>"
        )
    else:
        raise ValueError("Unknown plot_type – expected 'hist', 'box', or 'scatter'.")

    parts: List[str] = [f"<h3 class='mt-3'>{title}</h3><div class='row'>"]
    for col, b64 in imgs:
        parts.append(
            "<div class='col-md-4 mb-3'>"
            f"<img class='img-fluid' src='data:image/png;base64,{b64}' alt='{col}'>"
            "</div>"
        )
    parts.append("</div>")
    return "".join(parts)
