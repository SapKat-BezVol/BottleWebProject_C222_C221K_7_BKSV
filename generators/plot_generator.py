"""
Генератор HTML‑фрагментов с визуализациями — гистограммами,
box‑plot, scatter‑matrix — для числовых столбцов таблицы *pandas*.

Экспортируемые элементы
-----------------------
build_plot_html
    Центральная точка входа, возвращающая готовый HTML‑код выбранного
    типа графиков ("hist", "box", "scatter").
"""

from __future__ import annotations

# --- Стандартная библиотека ---
import base64
import io
import os
import uuid
from typing import Dict, List, Tuple

# --- Сторонние библиотеки ---
import matplotlib

matplotlib.use("Agg")  
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix

__all__ = ["build_plot_html"]  # Ограничиваем публичный интерфейс модуля

# ---------------------------------------------------------------------------
#   Вспомогательные функции
# ---------------------------------------------------------------------------

def _fig_to_base64(fig: plt.Figure) -> str:
    """Преобразовать объект *Figure* в строку base64.

    Args:
        fig: Объект matplotlib *Figure*.

    Returns:
        Base64‑закодированная PNG‑картинка без переноса строк.
    """
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")


def _save_html_file(content: str, base_name: str) -> None:
    """Сохранить HTML‑контент в файл с уникальным суффиксом.

    Файлы кладутся в директорию ``data/variant3``; при отсутствии каталога
    он создаётся.

    Args:
        content: Готовый HTML‑код.
        base_name: Базовое имя файла без расширения.
    """
    os.makedirs("data/variant3", exist_ok=True)
    uid = uuid.uuid4().hex[:8]  # короткий уникальный идентификатор
    filename = f"{base_name}_{uid}.html"
    filepath = os.path.join("data/variant3", filename)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)


# Словарь русских описаний к статистическим ключам
_HIST_DESCRIPTIONS: Dict[str, str] = {
    "count": "Количество наблюдений",
    "mean": "Среднее арифметическое",
    "median": "Медиана (50‑й перцентиль)",
    "std": "Стандартное отклонение",
    "min": "Минимальное значение",
    "max": "Максимальное значение",
}


def _basic_hist_stats(series: pd.Series) -> Dict[str, float]:
    """Посчитать базовые статистики для столбца.

    Args:
        series: Числовой столбец DataFrame.

    Returns:
        Словарь со статистическими метриками.
    """
    return {
        "count": series.count(),
        "mean": series.mean(),
        "median": series.median(),
        "std": series.std(),
        "min": series.min(),
        "max": series.max(),
    }


def _hist_stats_table(stats: Dict[str, float]) -> str:
    """Сгенерировать HTML‑таблицу из статистик гистограммы."""
    rows: List[str] = []
    for key, val in stats.items():
        descr = _HIST_DESCRIPTIONS.get(key, key)
        num = f"{val:.4f}" if isinstance(val, (int, float, np.floating)) else val
        rows.append(f"<tr><td>{key}</td><td>{descr}</td><td>{num}</td></tr>")
    return (
        "<table class='table table-bordered table-sm'>"
        "<thead><tr><th>Код</th><th>Описание</th><th>Значение</th></tr></thead>"
        "<tbody>" + "\n".join(rows) + "</tbody></table>"
    )


def _box_stats_table(stats: Dict[str, Dict[str, float]]) -> str:
    """Сгенерировать HTML‑таблицу статистик для box‑plot."""
    header = (
        "<tr><th>Столбец</th><th>Минимум</th><th>Q1 (25 %)</th>"
        "<th>Медиана</th><th>Q3 (75 %)</th><th>Максимум</th>"
        "<th>IQR</th><th>Выбросы %</th></tr>"
    )
    body_rows: List[str] = []
    for col, st in stats.items():
        row = (
            "<tr>"
            f"<td>{col}</td><td>{st['min']:.4f}</td><td>{st['q1']:.4f}</td>"
            f"<td>{st['median']:.4f}</td><td>{st['q3']:.4f}</td>"
            f"<td>{st['max']:.4f}</td><td>{st['iqr']:.4f}</td>"
            f"<td>{st['outliers_percent']:.2f}</td></tr>"
        )
        body_rows.append(row)
    return (
        "<table class='table table-bordered table-sm table-scroll'>"
        "<thead>" + header + "</thead><tbody>" + "\n".join(body_rows) + "</tbody></table>"
    )

# ---------------------------------------------------------------------------
#   Генераторы конкретных графиков
# ---------------------------------------------------------------------------

def _build_histograms(df: pd.DataFrame) -> List[Tuple[str, str, str]]:
    """Построить гистограммы для всех числовых столбцов.

    Args:
        df: Входной *DataFrame*.

    Returns:
        Список кортежей *(col_name, base64_img, stats_html)*.

    Raises:
        ValueError: Если нет числовых столбцов.
    """
    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        raise ValueError("Нет числовых столбцов для гистограмм.")

    outs: List[Tuple[str, str, str]] = []
    for col in numeric.columns:
        # --- График ---
        fig = plt.figure(figsize=(6, 4))
        numeric[col].hist(bins="auto", density=True, label="Распределение данных")
        plt.title(f"Гистограмма • {col}")
        plt.xlabel(col)
        plt.ylabel("Плотность")
        plt.legend()
        img64 = _fig_to_base64(fig)
        plt.close(fig)

        # --- Статистическая сводка ---
        stats_html = _hist_stats_table(_basic_hist_stats(numeric[col]))

        # --- Индивидуальный HTML‑отчёт ---
        html = f"""
        <html><head><meta charset='utf-8'><title>Гистограмма: {col}</title></head><body>
        <h3>Гистограмма: {col}</h3>
        <img src='data:image/png;base64,{img64}' alt='Гистограмма: {col}'>
        <hr>{stats_html}</body></html>
        """
        _save_html_file(html, f"histogram_{col}")

        outs.append((col, img64, stats_html))
    return outs


def _build_boxplots(df: pd.DataFrame) -> List[Tuple[str, str, str]]:
    """Построить единый box‑plot для всех числовых столбцов."""
    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        raise ValueError("Нет числовых столбцов для box‑plot.")

    # --- График ---
    fig = plt.figure(figsize=(8, 6))
    numeric.plot.box(ax=fig.add_subplot(1, 1, 1), vert=True)
    plt.title("Box‑plot всех числовых столбцов")
    plt.xlabel("Столбцы")
    plt.ylabel("Значения")
    img64 = _fig_to_base64(fig)
    plt.close(fig)

    # --- Расчёт статистик для таблицы ---
    stats: Dict[str, Dict[str, float]] = {}
    for col in numeric.columns:
        col_data = numeric[col].dropna()
        q1, q3 = col_data.quantile([0.25, 0.75])
        iqr = q3 - q1
        outliers = col_data[(col_data < q1 - 1.5 * iqr) | (col_data > q3 + 1.5 * iqr)]
        stats[col] = {
            "min": col_data.min(),
            "q1": q1,
            "median": col_data.median(),
            "q3": q3,
            "max": col_data.max(),
            "iqr": iqr,
            "outliers_percent": len(outliers) / len(col_data) * 100,
        }

    stats_html = _box_stats_table(stats)

    # --- Сохраняем индивидуальный отчёт ---
    html = f"""
    <html><head><meta charset='utf-8'><title>Box-plot</title></head><body>
    <h3>Box-plot всех числовых столбцов</h3>
    <img src='data:image/png;base64,{img64}' alt='Box-plot'>
    <hr>{stats_html}</body></html>
    """
    _save_html_file(html, "boxplot_all_columns")

    return [("Box-plot", img64, stats_html)]


def _build_scatter_matrix(df: pd.DataFrame) -> List[Tuple[str, str, str]]:
    """Построить scatter‑matrix и аннотировать коэффициенты корреляции."""
    numeric = df.select_dtypes(include="number")
    if numeric.shape[1] < 2:
        raise ValueError("Для scatter‑matrix нужно минимум два числовых столбца.")

    axes = scatter_matrix(numeric, figsize=(8, 8), diagonal="hist")
    corr = numeric.corr().values
    cols = numeric.columns
    # Аннотируем ячейки вне диагонали значениями корреляции
    for i in range(len(cols)):
        for j in range(len(cols)):
            if i == j:
                continue
            axes[i, j].annotate(
                f"ρ = {corr[i, j]:.2f}",
                xy=(0.95, 0.85),
                xycoords="axes fraction",
                ha="right",
                va="center",
                fontsize=8,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.7),
            )

    img64 = _fig_to_base64(axes[0, 0].get_figure())
    plt.close(axes[0, 0].get_figure())

    # Отдельный HTML‑файл отчёта
    html = f"""
    <html><head><meta charset='utf-8'><title>Scatter Matrix</title></head><body>
    <h3>Scatter-matrix для числовых признаков</h3>
    <img src='data:image/png;base64,{img64}' alt='Scatter-matrix'>
    </body></html>
    """
    _save_html_file(html, "scatter_matrix")

    return [("Scatter-matrix", img64, "")]

# ---------------------------------------------------------------------------
#   Главная функция‑обёртка
# ---------------------------------------------------------------------------

def build_plot_html(df: pd.DataFrame, plot_type: str) -> str:
    """Сформировать HTML‑блок с визуализациями.

    Args:
        df: Входной набор данных.
        plot_type: Один из ``{"hist", "box", "scatter"}``.

    Returns:
        HTML‑фрагмент, который можно отдать фронтенду.

    Raises:
        ValueError: Если ``plot_type`` не поддерживается.
    """
    builders = {
        "hist": (_build_histograms, "Гистограммы"),
        "box": (_build_boxplots, "Box-plot"),
        "scatter": (_build_scatter_matrix, "Scatter-matrix"),
    }
    if plot_type not in builders:
        raise ValueError(f"Неизвестный plot_type: {plot_type!r}")

    build_func, title = builders[plot_type]
    items = build_func(df)  # Генерируем графики

    # --- Сборка карточек Bootstrap ---
    html_parts: List[str] = [
        "<style>html,body{margin:0;padding:0;overflow:hidden}</style>",
        f"<h3 class='mt-3 mb-4'>{title}</h3>",
    ]

    for label, img64, stats_html in items:
        card_title = label if plot_type == "hist" else title
        if plot_type == "box":
            # Box‑plot содержит одну общую картинку + таблицу статистик
            html_parts.append(
                f"""
                <div class='card mb-4'>
                  <div class='card-body text-center'>
                    <img class='img-fluid d-block mx-auto'
                         src='data:image/png;base64,{img64}' alt='{card_title}'>
                    <div class='mt-3'>{stats_html}</div>
                  </div>
                </div>
                """
            )
        else:
            # Гистограммы / scatter‑matrix могут иметь таблицу или нет
            stats_block = f"<div class='col-md-6'>{stats_html}</div>" if stats_html else ""
            html_parts.append(
                f"""
                <div class='card mb-4'>
                  <div class='card-body'>
                    <div class='row justify-content-center'>
                      <div class='col-md-6 text-center'>
                        <img class='img-fluid d-block mx-auto'
                             src='data:image/png;base64,{img64}' alt='{card_title}'>
                      </div>
                      {stats_block}
                    </div>
                  </div>
                </div>
                """
            )

    return "\n".join(html_parts) + "<footer>Generated by Mister Semya</footer>"