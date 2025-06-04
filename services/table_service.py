"""
Сервис работы с таблицами: генерация/загрузка и выборка строк.

Зависимости:
    * utils.table_maker.build_table
    * pandas
"""

from __future__ import annotations

import html
from typing import Tuple, Optional

import pandas as pd

from utils.table_maker import build_table


# -----------------------------------------------------------------------------
#   Генерация или загрузка таблицы
# -----------------------------------------------------------------------------
def generate_table(  # noqa: WPS211
    mode: str,
    upload_file,
    rows: int | None = None,
    cols: int | None = None,
    pattern: str | None = None,
) -> Tuple[str, Optional[pd.DataFrame]]:
    """
    Сгенерировать либо загрузить таблицу.

    Возвращает HTML-фрагмент (успех / ошибка) и сам DataFrame
    (``None`` при ошибке).

    Параметры:
        mode:  ``"upload"`` | любой другой (генерация случайных данных)
        upload_file:  объект Bottle FileUpload (или ``None``)
        rows, cols, pattern:  параметры генерации при mode ≠ "upload"
    """
    _, error_html, df = build_table(mode, upload_file, rows, cols, pattern)
    if error_html:
        return error_html, None

    success_msg = (
        "Файл успешно загружен и таблица построена."
        if mode == "upload"
        else "Таблица успешно сгенерирована."
    )
    return (
        f"<div class='alert alert-info'>{success_msg}</div>",
        df,
    )


# -----------------------------------------------------------------------------
#   Получение выборки из таблицы
# -----------------------------------------------------------------------------
def build_sample_html(df: pd.DataFrame, n: int = 5, mode: str = "head") -> str:
    """
    Вернуть HTML-страницу с выборкой ``n`` строк из ``df``.

    mode:
        * head   — первые n строк
        * tail   — последние n строки
        * random — случайные n строки
    """
    warning_msg = ""

    if n < 1:
        warning_msg = f"<div class='alert alert-warning'>Значение n={n} не должно быть меньше 1.</div>"
        n = 1
    elif n > len(df):
        warning_msg = f"<div class='alert alert-warning'>Значение n={n} превышает количество строк {len(df)} в таблице.</div>"
        n = len(df)

    if mode == "head":
        sample_df = df.head(n)
    elif mode == "tail":
        sample_df = df.tail(n)
    elif mode == "random":
        sample_df = df.sample(n)
    else:
        return (
            "<div class='alert alert-danger'>Некорректный режим отображения</div>"
        )

    table_html = sample_df.to_html(
        classes="table table-bordered table-hover table-striped w-100",
        index=False,
        border=0,
    )

    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"  rel="stylesheet">
        <style>body{{margin:0;padding:1rem}}</style>
    </head>
    <body>
        {warning_msg}
        <h5>Отображаемые данные ({html.escape(mode)}, {n} записей):</h5>
        {table_html}
    </body>
    </html>
    """