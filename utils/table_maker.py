from __future__ import annotations

"""
Вспомогательные функции для чтения пользовательских данных и отображения их
в виде адаптивной HTML‑таблицы.

Содержит три публичных элемента:

* :func:`build_table` — формирует HTML‑таблицу из загруженного файла или
  синтетически сгенерированного DataFrame.
* :func:`render_page` — оборачивает результат работы `build_table` в полный
  HTML‑документ, готовый к отдаче во фронтенд/браузер.
* Вспомогательная _parse_upload (не экспортируется) — преобразует загруженный
  пользователем файл (CSV/TSV/JSON) в :class:`pandas.DataFrame`
"""

from io import BytesIO
from typing import Optional, Tuple
import html

import pandas as pd

from utils.data_loader import load_data

__all__ = ["build_table", "render_page"]


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _parse_upload(upload_file) -> pd.DataFrame:
    """Создаёт :class:`pandas.DataFrame` из загруженного пользователем файла.

    Args:
        upload_file: Объект, возвращаемый компонентом загрузки. Предполагается,
            что у него есть как минимум два атрибута:

            * ``filename`` — строка с именем файла; используется для определения
              расширения.
            * ``file`` — файловоподобный объект, открытый в бинарном режиме,
              чьё содержимое будет считываться.

    Returns:
        pd.DataFrame: Считанные из файла данные.

    Raises:
        ValueError: Если файл не выбран или его тип не поддерживается.
    """

    # Проверяем, что файл действительно передан и имя не пустое
    if not (upload_file and upload_file.filename):
        raise ValueError("Файл не выбран.")

    # Определяем расширение и нормализуем к нижнему регистру для надёжности
    ext = upload_file.filename.rsplit(".", 1)[-1].lower()

    # Читаем содержимое файла как bytes (важно для BytesIO)
    raw_bytes: bytes = upload_file.file.read()
    # Простейшая защита от загрузки чрезмерно больших файлов
    if len(raw_bytes) > 5 * 1024 * 1024:  # 5 MB
        raise ValueError("Размер файла превышает 5 МБ.")

    # Карта расширений к функциям‑парсерам pandas
    parser_map = {
        "csv": lambda b: pd.read_csv(BytesIO(b)),
        "tsv": lambda b: pd.read_csv(BytesIO(b), sep="\t"),
        "json": lambda b: pd.read_json(BytesIO(b)),
    }

    try:
        parser = parser_map[ext]
    except KeyError as exc:
        raise ValueError("Поддерживаются только файлы CSV, TSV или JSON.") from exc

    # Конкретный парсер возвращает DataFrame
    return parser(raw_bytes)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_table(
    mode: str,
    upload_file,
    rows: int = 100,
    cols: int = 5,
    pattern: str = "linear",
) -> Tuple[Optional[str], Optional[str], Optional[pd.DataFrame]]:
    """Формирует HTML‑таблицу на основе пользовательского ввода либо
    синтетически сгенерированных данных.

    Args:
        mode: Режим работы. Если ``"upload"`` — используется файл,
            переданный в ``upload_file``; любое другое значение инициирует
            генерацию фейковых данных.
        upload_file: Файловый объект с атрибутами ``filename`` и ``file``.
        rows: Количество строк для генерации, если ``mode`` ≠ ``"upload"``.
        cols: Количество столбцов для генерации, если ``mode`` ≠ ``"upload"``.
        pattern: Шаблон генерации (см. ``utils.data_loader.load_data``).

    Returns:
        Tuple[Optional[str], Optional[str], Optional[pd.DataFrame]]: Кортеж,
        содержащий (в указанном порядке):

        #. HTML‑код таблицы или ``None`` при ошибке;
        #. HTML‑код ошибки (Bootstrap‑alert) или ``None`` при успехе;
        #. Исходный DataFrame или ``None`` при ошибке.
    """

    try:
        if mode == "upload":
            # Пытаемся прочитать файл пользователя.
            df = _parse_upload(upload_file)
        else:
            # Валидация параметров генерации.
            if not 1 <= rows <= 1000:
                raise ValueError("Количество строк должно быть от 1 до 1000.")
            if not 1 <= cols <= 10:
                raise ValueError("Количество столбцов должно быть от 1 до 10.")

            # Генерируем DataFrame с помощью вспомогательной функции.
            df = load_data(rows=rows, cols=cols, pattern=pattern)

        # Преобразуем DataFrame в HTML с bootstrap‑классами для красивого вида.
        table_html = df.to_html(
            classes="table table-bordered table-hover table-striped w-100",
            index=False,
            border=0,
            max_rows=None,
            max_cols=None,
        )
        return table_html, None, df

    except Exception as exc:
        # Оборачиваем текст ошибки в Bootstrap‑alert, экранируя текст
        safe_exc = html.escape(str(exc))
        error_html = f"<div class='alert alert-danger'>{safe_exc}</div>"
        return None, error_html, None


def render_page(table_html: Optional[str], error_html: Optional[str]) -> str:
    """Формирует полный HTML‑документ со встроенной таблицей или сообщением
    об ошибке.

    Args:
        table_html: Готовый фрагмент таблицы, возвращаемый :func:`build_table`.
        error_html: Фрагмент с сообщением об ошибке от :func:`build_table`.

    Returns:
        str: Строка‑HTML, готовая к отдаче во фронтенд или на запись в файл.
    """

    # Решаем, какой блок вставлять — таблицу или ошибку; если оба None, будет
    # вставлена пустая строка.
    body_content = (
        f"<div class='table-responsive'>{table_html}</div>" if table_html else error_html or ""
    )

    # Финальный HTML с подключённым Bootstrap 5.
    return f"""
        <!DOCTYPE html>
        <html lang=\"ru\">
        <head>
            <meta charset=\"utf-8\">
            <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
            <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">
            <style>
                body {{
                    margin: 0;
                    padding: 1rem;
                    box-sizing: border-box;
                    font-family: sans-serif;
                }}
                .table-responsive {{
                    overflow-x: auto;
                    white-space: nowrap;
                }}
                table {{
                    width: 100% !important;
                    table-layout: auto;
                }}
            </style>
        </head>
        <body>
            <div class=\"container-fluid\">
                {body_content}
            </div>
        </body>
        </html>
    """
