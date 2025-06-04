"""
Сервис анализа распределений.
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

import pandas as pd

from generators.distrib_generator import generate_distribution_html


def build_distribution_report(df: pd.DataFrame) -> str:
    """
    Сформировать отчёт о распределениях и сохранить его.

    Возвращает HTML-отчёт (готов к отображению пользователю).
    """
    html_report = generate_distribution_html(df)

    save_dir = Path("data") / "variant1"
    save_dir.mkdir(parents=True, exist_ok=True)

    filename = f"distribution_analysis_{datetime.now():%Y%m%d_%H%M%S}.html"
    (save_dir / filename).write_text(html_report, encoding="utf-8")

    return html_report
