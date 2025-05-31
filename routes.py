from __future__ import annotations

import pandas as pd
import numpy as np
from datetime import datetime
from io import BytesIO
from bottle import route, template, view, request, response
from sklearn.linear_model import LinearRegression

from utils.table_maker import build_table, _parse_upload, render_page, load_data
from services.correlation_generator import build_correlation_table,build_correlation_heatmap, analyze_correlations
from services.plot_generator import build_plot_html
from services.prediction_generator import build_prediction_numbers

generated_df: pd.DataFrame | None = None

@route('/')
@route('/home')
@view('index')
def home():
    """Рендер домашней страницы."""
    return dict(
        year=datetime.now().year
    )

@route('/about')
@view('about')
def about():
    """Рендер страницы с информацией о команде."""
    return dict(
        year=datetime.now().year
    )

@route('/show_sample', method='POST')
def show_sample():
    global generated_df
    if generated_df is None:
        return """
        <html><body>
        <div class='alert alert-danger'>Сначала сгенерируйте или загрузите таблицу</div>
        </body></html>
        """

    try:
        n = int(request.forms.get('n', 5))
        n = max(1, min(n, len(generated_df)))
        mode = request.forms.get('mode', 'head')

        if mode == 'head':
            sample_df = generated_df.head(n)
        elif mode == 'tail':
            sample_df = generated_df.tail(n)
        elif mode == 'random':
            sample_df = generated_df.sample(n)
        else:
            return """
            <html><body>
            <div class='alert alert-danger'>Некорректный режим отображения</div>
            </body></html>
            """
        sample_html = sample_df.to_html(classes='table table-bordered table-hover table-striped w-100', index=False, border=0)
        return f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{
                    margin: 0;
                    padding: 1rem;
                    box-sizing: border-box;
                }}
                table {{
                    width: 100% !important;
                    table-layout: auto;
                }}
            </style>
        </head>
        <body>
            <h5>Отображаемые данные ({mode}, {n} записей):</h5>
            {sample_html}
        </body>
        </html>
        """

    except Exception as e:
        return f"""
        <!DOCTYPE html>
        <html><body>
        <div class='alert alert-danger'>Ошибка: {e}</div>
        </body></html>
        """


@route('/generate_table', method='POST')
def generate_table():
    """
    Возвращает *только* сообщение об успехе – таблица не выводится,
    но сохраняется в глобальной переменной generated_df.
    """
    global generated_df
    try:
        mode = request.forms.get('mode')

        if mode == 'upload':
            upload_file = request.files.get('csv_file')
            _, error_html, df = build_table(mode, upload_file)
        else:
            rows = int(request.forms.get('rows', 100))
            cols = int(request.forms.get('cols', 5))
            pattern = request.forms.get('pattern', 'linear')
            _, error_html, df = build_table(mode, None, rows, cols, pattern)

        if error_html:
            return error_html

        generated_df = df
        return "<p class='text-success'>Таблица обработана.</p>"
        success_msg = (
            "Файл успешно загружен и таблица построена."
            if mode == 'upload'
            else "Таблица успешно сгенерирована."
        )
        return (
            f"<!DOCTYPE html><html><head>"
            f"<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>"
            f"</head><body><div class='alert alert-success'>{success_msg}</div></body></html>"
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return (
            "<!DOCTYPE html><html><head>"
            "<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>"
            "</head><body>"
            f"<div class='alert alert-danger'>Внутренняя ошибка сервера: {e}</div>"
            "</body></html>"
        )



@route("/generate_correlation", method="POST")
def generate_correlation_route() -> str:
    global generated_df
    if generated_df is None:
        error_html = "<div class='alert alert-danger'>Сначала сгенерируйте или загрузите таблицу</div>"
        return render_page("", error_html)

    try:
        numeric_df = generated_df.select_dtypes(include='number')
        if numeric_df.shape[1] < 2:
            raise ValueError("Недостаточно числовых столбцов для анализа корреляций (нужно минимум 2).")

        corr_matrix = numeric_df.corr()

        if corr_matrix.shape[0] != corr_matrix.shape[1]:
            raise ValueError("Ошибка: матрица корреляций не квадратная. Проверьте данные.")

        table_html = build_correlation_table(generated_df)
        heatmap_html = build_correlation_heatmap(generated_df)
        analysis_html = analyze_correlations(generated_df)
        combined_html = table_html + heatmap_html + analysis_html
        error_html = None
    except Exception as exc:
        combined_html = None
        error_html = f"<div class='alert alert-danger'>{exc}</div>"

    response.content_type = "text/html; charset=utf-8"
    return render_page(combined_html, error_html)



@route("/generate_plot", method="POST")
def generate_plot_route() -> str:
    global generated_df
    if generated_df is None:
        error_html = "<div class='alert alert-danger'>Сначала сгенерируйте или загрузите таблицу</div>"
        return render_page("", error_html)

    plot_type = request.forms.get("plot_type")
    try:
        html_snippet = build_plot_html(generated_df, plot_type)
        error_html = None
    except Exception as exc:
        html_snippet = ""
        error_html = f"<div class='alert alert-danger'>Ошибка: {exc}</div>"

    response.content_type = "text/html; charset=utf-8"
    return render_page(html_snippet, error_html)


@route("/make_prediction", method="POST")
def make_prediction_route() -> str:
    global generated_df
    if generated_df is None:
        error_html = "<div class='alert alert-danger'>Сначала сгенерируйте или загрузите таблицу</div>"
        return render_page("", error_html)

    try:
        prediction_html = build_prediction_numbers(generated_df)
        error_html = None
    except Exception as exc:
        error_html = f"<div class='alert alert-danger'>{exc}</div>"

        response.content_type = "text/html; charset=utf-8"
    return render_page(prediction_html, error_html)


@route('/generate_distributions', method='POST')
def generate_distributions():
    global generated_df
    if generated_df is None:
        return "<div class='alert alert-danger'>Сначала сгенерируйте или загрузите таблицу</div>"
    
    try:
        from services.distrib_generator import generate_distribution_html
        html = generate_distribution_html(generated_df)
        return html
    except Exception as e:
        return f"<div class='alert alert-danger'>Ошибка: {str(e)}</div>"


@route('/variant1', method='GET')
@view('variant1')
def variant1_page():
    """Рендер страницы для первого варианта."""
    return dict(
            year=datetime.now().year
    )


@route('/variant2', method=['GET', 'POST'])
@view('variant2')
def variant2():
    """Рендер страницы для второго варианта."""
    return dict(
            year=datetime.now().year
    )


@route('/variant3')
@view('variant3')
def about():
    """Рендер страницы для третьего варианта."""
    return dict(
        year=datetime.now().year
    )


@route('/variant4')
@view('variant4')
def about():
    """Рендер страницы для четвёртого варианта."""
    return dict(
        year=datetime.now().year
    )