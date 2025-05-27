from __future__ import annotations

import base64
import io
from typing import Optional

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def _fig_to_base64(fig: plt.Figure) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")


def build_correlation_plot(df: pd.DataFrame) -> str:
    corr_matrix = df.corr(numeric_only=True)
    print("DEBUG corr_matrix:")
    print(corr_matrix)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    plt.title("Correlation Heatmap")
    b64 = _fig_to_base64(fig)
    plt.close(fig)

    return (
        "<h3 class='mt-3'>Correlation Heatmap</h3>"
        f"<img class='img-fluid' src='data:image/png;base64,{b64}' alt='heatmap'>"
    )
