"""
Сервис корреляционного анализа.

Основные функции:
    * build_correlation_report — формирование отчёта + сохранение в файл
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pandas as pd

from generators.correlation_generator import (
    build_correlation_html,
    save_correlation_report,
)


def build_correlation_report(df: pd.DataFrame) -> Tuple[str, str]:
    """
    Выполнить корреляционный анализ и вернуть пару
    (полный HTML-отчёт, HTML-сообщение-уведомление).

    Исключения пробрасываются наружу.
    """
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.shape[1] < 2:
        raise ValueError(
            "Недостаточно числовых столбцов для анализа (нужно ≥ 2).",
        )

    # Генерация отчёта
    report_html: str = build_correlation_html(df)

    # Сохранение на диск
    file_path: Path = save_correlation_report(report_html)
    info_html = (
        "<div class='alert alert-info'>Отчёт сохранён: "
        f"<code>{file_path}</code></div>"
    )

    return report_html, info_html
