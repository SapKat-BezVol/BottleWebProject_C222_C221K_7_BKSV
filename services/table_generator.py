from __future__ import annotations

from io import BytesIO
from typing import Tuple, Optional
import pandas as pd
from utils.data_loader import load_data


def _parse_upload(upload_file) -> pd.DataFrame:
    """
    Обрабатывает загруженный пользователем файл (CSV, TSV или JSON) и возвращает DataFrame.

    Параметры:
        upload_file: файл, загруженный пользователем (должен иметь атрибуты `filename` и `file`)

    Возвращает:
        DataFrame с данными из файла
    """
    if not (upload_file and upload_file.filename):
        raise ValueError("Файл не выбран.")  # Проверка на наличие файла

    ext = upload_file.filename.rsplit(".", 1)[-1].lower()  # Получаем расширение файла
    raw = upload_file.file.read()  # Читаем содержимое файла как байты

    # Сопоставление расширений с соответствующим методом чтения в pandas
    parser_map = {
        "csv": lambda b: pd.read_csv(BytesIO(b)),
        "tsv": lambda b: pd.read_csv(BytesIO(b), sep="\t"),
        "json": lambda b: pd.read_json(BytesIO(b)),
    }

    try:
        parser = parser_map[ext]  # Выбираем подходящий парсер
    except KeyError:
        raise ValueError("Поддерживаются файлы CSV, TSV или JSON.") from None

    return parser(raw)  # Возвращаем DataFrame


def build_table(
    mode: str,
    upload_file,
    rows: int = 100,
    cols: int = 5,
    pattern: str = "linear"
) -> Tuple[Optional[str], Optional[str], Optional[pd.DataFrame]]:
    """
    Создаёт HTML-таблицу из пользовательского файла или синтетических данных.

    Параметры:
        mode: 'upload' — загруженный файл, иначе — генерация
        upload_file: файл, загруженный пользователем
        rows: количество строк для генерации (если не upload)
        cols: количество столбцов для генерации (если не upload)
        pattern: шаблон для генерации данных (если не upload)

    Возвращает:
        Кортеж из HTML-таблицы (или None), HTML-ошибки (или None), и самого DataFrame (или None)
    """
    try:
        if mode == "upload":
            df = _parse_upload(upload_file)  # Загружаем пользовательский файл
        else:
            # Проверка валидности параметров генерации
            if not 1 <= rows <= 1000:
                raise ValueError("Количество строк должно быть от 1 до 1000.")
            if not 1 <= cols <= 10:
                raise ValueError("Количество столбцов должно быть от 1 до 10.")
            df = load_data(rows=rows, cols=cols, pattern=pattern)  # Генерация данных

        # Преобразуем DataFrame в HTML-таблицу с Bootstrap-классами
        table_html = df.to_html(
            classes="table table-striped table-bordered",  # Стиль таблицы
            index=False,  # Не отображать индекс
            border=0,
            max_rows=None,
            max_cols=None,
        )
        return table_html, None, df  # Возвращаем HTML и DataFrame

    except Exception as exc:
        error_html = f"<div class='alert alert-danger'>{exc}</div>"  # Оборачиваем ошибку в Bootstrap-алерт
        return None, error_html, None  # Возвращаем ошибку


def render_page(table_html: Optional[str], error_html: Optional[str]) -> str:
    """
    Оборачивает результат (таблицу или ошибку) в простую HTML-страницу с Bootstrap.

    Параметры:
        table_html: HTML-код таблицы (если есть)
        error_html: HTML-код ошибки (если есть)

    Возвращает:
        Полноценный HTML-документ для отображения в браузере
    """
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css'>"
        "<style>.table-scroll{max-height:80vh;overflow:auto;}</style>"
        "</head><body>"
        f"<div class='table-scroll table-responsive'>{table_html or error_html or ''}</div>"
        "</body></html>"
    )
