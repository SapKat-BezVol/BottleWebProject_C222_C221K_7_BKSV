"""
HTTP-маршруты Bottle-приложения
"""

from __future__ import annotations

import logging
import traceback
from datetime import datetime
from typing import List

import pandas as pd
from bottle import request, response, route, view

# --- Внутренние пакеты -------------------------------------------------------
from utils.table_maker import render_page
from services.table_service import generate_table, build_sample_html
from services.correlation_service import build_correlation_report
from services.plot_service import build_plot
from services.prediction_service import build_prediction, save_prediction
from services.distribution_service import build_distribution_report

# -----------------------------------------------------------------------------
#   Глобальное хранилище текущего набора данных
# -----------------------------------------------------------------------------
generated_df: pd.DataFrame | None = None

# -----------------------------------------------------------------------------
#   Базовые статические страницы
# -----------------------------------------------------------------------------
@route("/")
@route("/home")
@view("base/index")
def home() -> dict[str, int]:
    """Домашняя страница."""
    return {"year": datetime.now().year}


@route("/about")
@view("base/about")
def about() -> dict[str, int]:
    """Страница «О команде»."""
    return {"year": datetime.now().year}


# -----------------------------------------------------------------------------
#   Работа с таблицами
# -----------------------------------------------------------------------------
@route("/show_sample", method="POST")
def show_sample() -> str:
    """Показать выборку строк из текущей таблицы."""
    global generated_df  # noqa: WPS420

    if generated_df is None:
        return (
            "<div class='alert alert-danger'>Сначала сгенерируйте или загрузите "
            "таблицу</div>"
        )

    try:
        n = int(request.forms.get("n", 5))
        mode = request.forms.get("mode", "head")
        return build_sample_html(generated_df, n, mode)
    except Exception:  # noqa: WPS440
        logging.error("Ошибка в show_sample", exc_info=True)
        return (
            "<div class='alert alert-danger'>Внутренняя ошибка сервера. "
            "Пожалуйста, попробуйте позже.</div>"
        )


@route("/generate_table", method="POST")
def generate_table_route() -> str:
    """Загрузить CSV либо сгенерировать случайную таблицу."""
    global generated_df  # noqa: WPS420

    try:
        mode = request.forms.get("mode")
        if mode == "upload":
            upload_file = request.files.get("csv_file")
            message_html, df = generate_table(mode, upload_file)
        else:
            rows = int(request.forms.get("rows", 100))
            cols = int(request.forms.get("cols", 5))
            pattern = request.forms.get("pattern", "linear")
            message_html, df = generate_table(
                mode,
                None,
                rows=rows,
                cols=cols,
                pattern=pattern,
            )

        if df is not None:
            generated_df = df

        # Минимальная страница-обёртка (загружается во <iframe>)
        return (
            "<!DOCTYPE html><html><head>"
            "<meta charset='utf-8'>"
            "<link rel='stylesheet' href='/static/content/bootstrap.min.css'>"
            "<style>html,body{margin:0;padding:0;overflow:hidden}</style>"
            "</head><body>"
            f"{message_html}"
            "</body></html>"
        )
    except Exception:  # noqa: WPS440
        traceback.print_exc()
        logging.error("Ошибка в generate_table_route", exc_info=True)
        return (
            "<div class='alert alert-danger'>Внутренняя ошибка сервера. "
            "Пожалуйста, попробуйте позже.</div>"
        )


# -----------------------------------------------------------------------------
#   Корреляционный анализ
# -----------------------------------------------------------------------------
@route("/generate_correlation", method="POST")
def generate_correlation_route() -> str:
    """Сформировать отчёт о корреляциях."""
    global generated_df  # noqa: WPS420

    if generated_df is None:
        error_html = (
            "<div class='alert alert-danger'>Сначала сгенерируйте или загрузите "
            "таблицу</div>"
        )
        return render_page("", error_html)

    try:
        report_html, info_html = build_correlation_report(generated_df)
        response.content_type = "text/html; charset=utf-8"
        return render_page(report_html, info_html)
    except Exception as exc:  # noqa: WPS440
        error_html = f"<div class='alert alert-danger'>{exc}</div>"
        return render_page("", error_html)


# -----------------------------------------------------------------------------
#   Построение графиков
# -----------------------------------------------------------------------------
@route("/generate_plot", method="POST")
def generate_plot_route() -> str:
    """Построить график по текущему датасету."""
    global generated_df  # noqa: WPS420

    if generated_df is None:
        return render_page(
            "",
            "<div class='alert alert-danger'>Сначала сгенерируйте или "
            "загрузите таблицу</div>",
        )

    plot_type = request.forms.get("plot_type")
    html_snippet, error_html = build_plot(generated_df, plot_type)
    response.content_type = "text/html; charset=utf-8"
    return render_page(html_snippet, error_html)


# -----------------------------------------------------------------------------
#   Прогнозирование
# -----------------------------------------------------------------------------
@route("/make_prediction", method="POST")
def make_prediction_route() -> str:
    """Сделать прогноз и отобразить результат."""
    global generated_df  # noqa: WPS420

    if generated_df is None:
        return render_page(
            "",
            "<div class='alert alert-danger'>Сначала сгенерируйте или "
            "загрузите таблицу</div>",
        )

    html_block, error_html = build_prediction(generated_df)
    response.content_type = "text/html; charset=utf-8"
    return render_page(html_block, error_html)


@route("/save_prediction", method="POST")
def save_prediction_route() -> str:
    """Сохранить результаты предсказания вместе с датасетом."""
    global generated_df  # noqa: WPS420

    if generated_df is None:
        return "<div class='alert alert-danger'>Нет данных для сохранения</div>"

    try:
        target_col = int(request.forms.get("target_col")) - 1
        features_raw: List[str] = request.forms.get("features", "").split()
        features = [float(x) for x in features_raw]

        return save_prediction(generated_df, target_col, features)
    except Exception as exc:  # noqa: WPS440
        return f"<div class='alert alert-danger'>{exc}</div>"


# -----------------------------------------------------------------------------
#   Анализ распределений
# -----------------------------------------------------------------------------
@route("/generate_distributions", method="POST")
def generate_distributions_route() -> str:
    """Сформировать отчёт о распределениях признаков."""
    global generated_df  # noqa: WPS420

    if generated_df is None:
        return (
            "<div class='alert alert-danger'>Сначала сгенерируйте или "
            "загрузите таблицу</div>"
        )

    try:
        html_report = build_distribution_report(generated_df)
        response.content_type = "text/html; charset=utf-8"
        return html_report
    except Exception:  # noqa: WPS440
        logging.error("Ошибка в generate_distributions_route", exc_info=True)
        return (
            "<div class='alert alert-danger'>Внутренняя ошибка сервера. "
            "Пожалуйста, попробуйте позже.</div>"
        )


# -----------------------------------------------------------------------------
#   Учебные статические варианты
# -----------------------------------------------------------------------------
@route("/variant1")
@view("variants/variant1")
def variant1_page() -> dict[str, int]:
    """Учебная страница «Вариант 1»."""
    return {"year": datetime.now().year}


@route("/variant2", method=["GET", "POST"])
@view("variants/variant2")
def variant2_page() -> dict[str, int]:
    """Учебная страница «Вариант 2»."""
    return {"year": datetime.now().year}


@route("/variant3")
@view("variants/variant3")
def variant3_page() -> dict[str, int]:
    """Учебная страница «Вариант 3»."""
    return {"year": datetime.now().year}


@route("/variant4")
@view("variants/variant4")
def variant4_page() -> dict[str, int]:
    """Учебная страница «Вариант 4»."""
    return {"year": datetime.now().year}
