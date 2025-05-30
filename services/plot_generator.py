# -*- coding: utf-8 -*-
from __future__ import annotations

import base64
import io
from typing import Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix

__all__ = ["build_plot_html"]

def _fig_to_base64(fig: plt.Figure) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")

_HIST_DESCRIPTIONS: Dict[str, str] = {
    "count":   "Количество наблюдений",
    "mean":    "Среднее арифметическое",
    "median":  "Медиана (50-й перцентиль)",
    "std":     "Стандартное отклонение",
    "min":     "Минимальное значение",
    "max":     "Максимальное значение",
}

def _basic_hist_stats(series: pd.Series) -> Dict[str, float]:
    return {
        "count": series.count(),
        "mean":  series.mean(),
        "median": series.median(),
        "std":   series.std(),
        "min":   series.min(),
        "max":   series.max(),
    }

def _hist_stats_table(stats: Dict[str, float]) -> str:
    """Трёхколоночная таблица для гистограмм."""
    rows = []
    for key, val in stats.items():
        descr = _HIST_DESCRIPTIONS.get(key, key)
        num   = f"{val:.4f}" if isinstance(val, (int, float, np.floating)) else val
        rows.append(f"<tr><td>{key}</td><td>{descr}</td><td>{num}</td></tr>")
    return (
        "<table class='table table-bordered table-sm'>"
        "<thead><tr><th>Код</th><th>Описание</th><th>Значение</th></tr></thead>"
        "<tbody>" + "\n".join(rows) + "</tbody></table>"
    )

def _box_stats_table(stats: Dict[str, Dict[str, float]]) -> str:
    """Таблица, где каждая строка — отдельный столбец с квартилями и выбросами."""
    header = (
        "<tr>"
        "<th>Столбец</th><th>Минимум</th><th>Q1 (25 %)</th>"
        "<th>Медиана</th><th>Q3 (75 %)</th><th>Максимум</th>"
        "<th>IQR</th><th>Выбросы&nbsp;%</th>"
        "</tr>"
    )
    body_rows = []
    for col, st in stats.items():
        body_rows.append(
            "<tr>"
            f"<td>{col}</td>"
            f"<td>{st['min']:.4f}</td>"
            f"<td>{st['q1']:.4f}</td>"
            f"<td>{st['median']:.4f}</td>"
            f"<td>{st['q3']:.4f}</td>"
            f"<td>{st['max']:.4f}</td>"
            f"<td>{st['iqr']:.4f}</td>"
            f"<td>{st['outliers_percent']:.2f}</td>"
            "</tr>"
        )
    return (
        "<table class='table table-bordered table-sm table-scroll'>"
        "<thead>" + header + "</thead>"
        "<tbody>" + "\n".join(body_rows) + "</tbody></table>"
    )

def _build_histograms(df: pd.DataFrame) -> List[Tuple[str, str, str]]:
    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        raise ValueError("Нет числовых столбцов для гистограмм.")
    outs = []
    for col in numeric.columns:
        fig = plt.figure(figsize=(6, 4))
        numeric[col].hist(bins="auto", density=True, label="Распределение данных")
        plt.title(f"Гистограмма • {col}")
        plt.xlabel(col); plt.ylabel("Плотность")
        plt.legend()
        img64 = _fig_to_base64(fig)
        plt.close(fig)

        stats_html = _hist_stats_table(_basic_hist_stats(numeric[col]))
        outs.append((col, img64, stats_html))
    return outs

def _build_boxplots(df: pd.DataFrame) -> List[Tuple[str, str, str]]:
    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        raise ValueError("Нет числовых столбцов для box-plot.")
    fig = plt.figure(figsize=(8, 6))
    numeric.plot.box(ax=fig.add_subplot(1, 1, 1), vert=True)
    plt.title("Box-plot всех числовых столбцов")
    plt.xlabel("Столбцы"); plt.ylabel("Значения")
    img64 = _fig_to_base64(fig)
    plt.close(fig)

    stats: Dict[str, Dict[str, float]] = {}
    for col in numeric.columns:
        col_data = numeric[col].dropna()
        q1, q3 = col_data.quantile([0.25, 0.75])
        iqr = q3 - q1
        outliers = col_data[(col_data < q1 - 1.5 * iqr) | (col_data > q3 + 1.5 * iqr)]
        stats[col] = {
            "min":  col_data.min(),
            "q1":   q1,
            "median": col_data.median(),
            "q3":   q3,
            "max":  col_data.max(),
            "iqr":  iqr,
            "outliers_percent": len(outliers) / len(col_data) * 100,
        }
    stats_html = _box_stats_table(stats)
    return [("Box-plot", img64, stats_html)]

def _build_scatter_matrix(df: pd.DataFrame) -> List[Tuple[str, str, str]]:
    numeric = df.select_dtypes(include="number")
    if numeric.shape[1] < 2:
        raise ValueError("Для scatter-matrix нужно минимум два числовых столбца.")
    axes = scatter_matrix(numeric, figsize=(8, 8), diagonal="hist")
    fig = axes[0, 0].get_figure()
    img64 = _fig_to_base64(fig)
    plt.close(fig)
    return [("Scatter-matrix", img64, "")]

def build_plot_html(df: pd.DataFrame, plot_type: str) -> str:
    builders = {
        "hist":    (_build_histograms, "Гистограммы"),
        "box":     (_build_boxplots,   "Box-plot"),
        "scatter": (_build_scatter_matrix, "Scatter-matrix"),
    }
    if plot_type not in builders:
        raise ValueError(f"Неизвестный plot_type: {plot_type!r}")

    build_func, title = builders[plot_type]
    items = build_func(df)

    html_parts: List[str] = [f"<h3 class='mt-3 mb-4'>{title}</h3>"]
    for label, img64, stats_html in items:
        card_title = label if plot_type == "hist" else title
        stats_block = (
            f"<div class='col-md-6'>{stats_html}</div>"
            if stats_html else ""
        )
        html_parts.append(
            f"""
            <div class='card mb-4'>
              <div class='card-body'>
                <div class='row'>
                  <div class='col-md-{"6" if stats_block else "12"}'>
                    <img class='img-fluid' src='data:image/png;base64,{img64}' alt='{card_title}'>
                  </div>
                  {stats_block}
                </div>
              </div>
            </div>
            """
        )

    return "\n".join(html_parts)
