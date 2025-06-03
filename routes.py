"""
Используемые подпроцессы:
    * utils.table_maker: построение/загрузка таблицы.
    * services.correlation_generator: корреляционный анализ и отчёт.
    * services.plot_generator: построение графиков.
    * services.prediction_generator: прогнозирование.
    * services.distrib_generator: анализ распределений.
"""

from __future__ import annotations

# --- Стандартная библиотека ---
import os
from datetime import datetime
from io import BytesIO

# --- Сторонние библиотеки ---
import html
import numpy as np
import pandas as pd
from bottle import route, template, view, request, response


# --- Внутренние пакеты проекта ---
from utils.table_maker import (
    build_table,
    _parse_upload,
    render_page,
    load_data,
)
from services.correlation_generator import (
    build_correlation_table,
    build_correlation_heatmap,
    analyze_correlations,
    build_correlation_html,
    save_correlation_report,
)
from services.plot_generator import build_plot_html
from services.prediction_generator import build_prediction_numbers


# Глобальная переменная, содержащая текущую рабочую таблицу.
generated_df: pd.DataFrame | None = None


# ---------------------------------------------------------------------------
#   Базовые страницы
# ---------------------------------------------------------------------------

@route('/')
@route('/home')
@view('index')
def home() -> dict[str, int]:
    """Домашняя страница.

    Returns:
        dict[str, int]: Словарь с текущим годом, который будет доступен в
            шаблоне *index.tpl* как ``{{year}}``.
    """
    return {"year": datetime.now().year}


@route('/about')
@view('about')
def about() -> dict[str, int]:
    """Страница «О команде».

    Returns:
        dict[str, int]: Аналогично :pyfunc:`home`, содержит текущий год.
    """
    return {"year": datetime.now().year}


# ---------------------------------------------------------------------------
#   Работа с таблицами
# ---------------------------------------------------------------------------

@route('/show_sample', method='POST')
def show_sample() -> str:
    """Показать выборку из текущей таблицы.

    Ожидает параметры формы:
        n (int, optional): Количество строк (по умолчанию ``5``).
        mode (str, optional): Способ выборки: ``head`` | ``tail`` |
            ``random`` (по умолчанию ``head``).

    Returns:
        str: Готовый HTML‑фрагмент либо сообщение об ошибке.
    """
    global generated_df

    if generated_df is None:
        # Пользователь ещё не загрузил/сгенерировал таблицу
        return (
            """
            <html><body>
            <div class='alert alert-danger'>Сначала сгенерируйте или загрузите таблицу</div>
            </body></html>
            """
        )

    try:
        n = int(request.forms.get('n', 5))
        n = max(1, min(n, len(generated_df)))  # Ограничиваем диапазон
        mode = request.forms.get('mode', 'head')

        # Выбираем подтаблицу в зависимости от режима
        if mode == 'head':
            sample_df = generated_df.head(n)
        elif mode == 'tail':
            sample_df = generated_df.tail(n)
        elif mode == 'random':
            sample_df = generated_df.sample(n)
        else:
            return (
                """
                <html><body>
                <div class='alert alert-danger'>Некорректный режим отображения</div>
                </body></html>
                """
            )

        # Преобразуем DataFrame в HTML‑таблицу c нужными классами Bootstrap
        sample_html = sample_df.to_html(
            classes='table table-bordered table-hover table-striped w-100',
            index=False,
            border=0,
        )

        # Возвращаем минимальную HTML‑страницу; обычно это отдаётся как
        # фрагмент в <iframe> или вставляется через fetch() на клиенте.
        return f"""
        <!DOCTYPE html>
        <html lang=\"ru\">
        <head>
            <meta charset=\"utf-8\">
            <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
            <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">
            <style>
                body {{ margin: 0; padding: 1rem; box-sizing: border-box; }}
                table {{ width: 100% !important; table-layout: auto; }}
            </style>
        </head>
        <body>
            <h5>Отображаемые данные ({html.escape(mode)}, {n} записей):</h5>
            {sample_html}
        </body>
        </html>
        """

    except Exception as exc:
        import logging

        logging.error("An error occurred in show_sample", exc_info=True)
        return (
            """
            <!DOCTYPE html>
            <html><body>
            <div class='alert alert-danger'>Внутренняя ошибка сервера. Пожалуйста, попробуйте позже.</div>
            </body></html>
            """
        )


@route('/generate_table', method='POST')
def generate_table() -> str:
    """Загрузить либо сгенерировать таблицу и сохранить её в *generated_df*.

    Поведение зависит от параметра формы ``mode``:
        * ``upload`` — ожидается файл CSV в поле ``csv_file``.
        * Иначе — генерируется таблица случайных данных.

    Returns:
        str: HTML‑фрагмент с сообщением об успехе или ошибке.
    """
    global generated_df

    try:
        mode = request.forms.get('mode')

        if mode == 'upload':
            upload_file = request.files.get('csv_file')
            _, error_html, df = build_table(mode, upload_file)
            success_msg = 'Файл успешно загружен и таблица построена.'
        else:
            rows = int(request.forms.get('rows', 100))
            cols = int(request.forms.get('cols', 5))
            pattern = request.forms.get('pattern', 'linear')
            _, error_html, df = build_table(mode, None, rows, cols, pattern)
            success_msg = 'Таблица успешно сгенерирована.'

        if error_html:
            # build_table вернул HTML с описанием ошибки
            return error_html

        generated_df = df  # Сохраняем датасет глобально

        # Минимальная страница только с алертом
        return (
            '<!DOCTYPE html><html><head>'
            "<meta charset='utf-8'>"
            "<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>"
            '<style>html,body{margin:0;padding:0;overflow:hidden}</style>'
            '</head><body>'
            f"<div class='alert alert-info mb-0'>{success_msg}</div>"
            '</body></html>'
        )

    except Exception as exc:
        import traceback
        import logging

        traceback.print_exc()
        logging.error('An error occurred in generate_table', exc_info=True)
        return (
            '<!DOCTYPE html><html><head>'
            "<meta charset='utf-8'>"
            "<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>"
            '</head><body>'
            "<div class='alert alert-danger'>Внутренняя ошибка сервера. Пожалуйста, попробуйте позже.</div>"
            '</body></html>'
        )


# ---------------------------------------------------------------------------
#   Корреляционный анализ
# ---------------------------------------------------------------------------

@route('/generate_correlation', method='POST')
def generate_correlation_route() -> str:
    """Сформировать отчёт о корреляциях между числовыми столбцами.

    Returns:
        str: Полная HTML‑страница с тепловой картой, таблицей и ссылкой на
            сохранённый отчёт либо сообщение об ошибке.
    """
    global generated_df

@route("/generate_correlation", method="POST")
def generate_correlation_route() -> str:
    global generated_df  # Используем глобальную переменную с данными

    if generated_df is None:
        # Если данных нет — сообщаем об ошибке
        error_html = "<div class='alert alert-danger'>Сначала сгенерируйте или загрузите таблицу</div>"
        return render_page("", error_html)

    try:
        numeric_df = generated_df.select_dtypes(include='number')  # Оставляем только числовые столбцы

        if numeric_df.shape[1] < 2:
            raise ValueError("Недостаточно числовых столбцов для анализа корреляций (нужно минимум 2).")

        corr_matrix = numeric_df.corr()

        if corr_matrix.shape[0] != corr_matrix.shape[1]:
            raise ValueError("Ошибка: матрица корреляций не квадратная. Проверьте данные.")

        # Генерируем HTML-отчёт
        full_html = build_correlation_html(generated_df)

        # Сохраняем его в файл
        filepath = save_correlation_report(full_html)

        # Информационное сообщение о сохранении
        save_notice = f"<div class='alert alert-info'>Отчёт сохранён: <code>{filepath}</code></div>"

        error_html = save_notice
        combined_html = full_html
    except Exception as exc:
        combined_html = None
        error_html = f"<div class='alert alert-danger'>{exc}</div>"

    response.content_type = "text/html; charset=utf-8"  # Устанавливаем кодировку ответа
    return render_page(combined_html, error_html)       # Отправляем страницу пользователю



# ---------------------------------------------------------------------------
#   Построение графиков
# ---------------------------------------------------------------------------

@route('/generate_plot', method='POST')
def generate_plot_route() -> str:
    """Построить график того или иного типа по текущему датасету.

    Ожидает параметр ``plot_type`` (см. *services.plot_generator*).

    Returns:
        str: HTML‑фрагмент с графиком либо ошибкой.
    """
    global generated_df

    if generated_df is None:
        error_html = '<div class="alert alert-danger">Сначала сгенерируйте или загрузите таблицу</div>'
        return render_page('', error_html)

    plot_type = request.forms.get('plot_type')
    try:
        html_snippet = build_plot_html(generated_df, plot_type)
        error_html = None
    except Exception as exc:
        html_snippet = ''
        error_html = f'<div class="alert alert-danger">Ошибка: {exc}</div>'

    response.content_type = 'text/html; charset=utf-8'
    return render_page(html_snippet, error_html)


# ---------------------------------------------------------------------------
#   Прогнозирование
# ---------------------------------------------------------------------------

@route('/make_prediction', method='POST')
def make_prediction_route() -> str:
    """Сделать прогнозы на основе текущей таблицы.

    Returns:
        str: HTML‑фрагмент с числовым прогнозом либо описанием ошибки.
    """
    global generated_df

    if generated_df is None:
        error_html = '<div class="alert alert-danger">Сначала сгенерируйте или загрузите таблицу</div>'
        return render_page('', error_html)

    try:
        prediction_html = build_prediction_numbers(generated_df)
        error_html = None
    except Exception as exc:
        error_html = f'<div class="alert alert-danger">{exc}</div>'

    response.content_type = 'text/html; charset=utf-8'
    return render_page(prediction_html, error_html)


# ---------------------------------------------------------------------------
#   Анализ распределений
# ---------------------------------------------------------------------------

@route('/generate_distributions', method='POST')
def generate_distributions() -> str:
    """Сформировать и сохранить отчёт о распределениях признаков.

    Returns:
        str: HTML‑отчёт либо сообщение об ошибке.
    """
    global generated_df

    if generated_df is None:
        return '<div class="alert alert-danger">Сначала сгенерируйте или загрузите таблицу</div>'

    try:
        from services.distrib_generator import generate_distribution_html

        html_report = generate_distribution_html(generated_df)

        # Папка для сохранения отчётов
        save_dir = r'data\variant1'
        os.makedirs(save_dir, exist_ok=True)

        # Имя файла содержит дату/время генерации
        now_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'distribution_analysis_{now_str}.html'
        save_path = os.path.join(save_dir, filename)

        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(html_report)

        return html_report

    except Exception as exc:
        import logging

        logging.error('An error occurred while generating distributions', exc_info=True)
        return '<div class="alert alert-danger">Произошла внутренняя ошибка. Пожалуйста, попробуйте позже.</div>'


# ---------------------------------------------------------------------------
#   Статические страницы
# ---------------------------------------------------------------------------

@route('/variant1', method='GET')
@view('variant1')
def variant1_page() -> dict[str, int]:
    """Учебная страница «Вариант 1»."""
    return {"year": datetime.now().year}


@route('/variant2', method=['GET', 'POST'])
@view('variant2')
def variant2() -> dict[str, int]:
    """Учебная страница «Вариант 2»."""
    return {"year": datetime.now().year}


@route('/variant3')
@view('variant3')
def variant3() -> dict[str, int]:
    """Учебная страница «Вариант 3»."""
    return {"year": datetime.now().year}


@route('/variant4')
@view('variant4')
def variant4() -> dict[str, int]:
    """Учебная страница «Вариант 4»."""
    return {"year": datetime.now().year}