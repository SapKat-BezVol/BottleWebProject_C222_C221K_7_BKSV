"""
Сервис построения графиков.
"""

from __future__ import annotations

from typing import Tuple
import html

import pandas as pd

from generators.plot_generator import build_plot_html


def build_plot(df: pd.DataFrame, plot_type: str) -> Tuple[str, str | None]:
    """
    Вернуть (HTML-график, HTML-ошибка|None).
    """
    try:
        return build_plot_html(df, plot_type), None
    except Exception as exc:  # noqa: WPS440
        return "", f"<div class='alert alert-danger'>Ошибка: {html.escape(str(exc))}</div>"
