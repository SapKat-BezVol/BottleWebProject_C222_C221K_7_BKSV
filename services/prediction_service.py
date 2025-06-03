"""
Сервис прогнозирования и сохранения результатов.
"""

from __future__ import annotations

from typing import Tuple, List

import pandas as pd

from generators.prediction_generator import (
    build_prediction_numbers,
    build_prediction_numbers_,
    save_data_with_prediction,
)


# -----------------------------------------------------------------------------


def build_prediction(df: pd.DataFrame) -> Tuple[str, str | None]:
    """
    Сформировать числовой прогноз.

    Возвращает (HTML-фрагмент, HTML-ошибка|None).
    """
    try:
        html_block = build_prediction_numbers(df)
        return html_block, None
    except Exception as exc:  # noqa: WPS440
        return "", f"<div class='alert alert-danger'>{exc}</div>"


def save_prediction(
    df: pd.DataFrame,
    target_col: int,
    features: List[float],
) -> str:
    """
    Сохранить данные и результат предсказания.

    Возвращает HTML-строку-уведомление.
    """
    prediction_text = build_prediction_numbers_(df, target_col, features)
    save_data_with_prediction(df, prediction_text)
    return "<div class='alert alert-success'>Данные и результат успешно сохранены</div>"
