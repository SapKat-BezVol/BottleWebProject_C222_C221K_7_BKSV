from __future__ import annotations

from datetime import datetime
from io import BytesIO
from typing import Tuple, Optional
from bottle import route, view, request, response
import pandas as pd
from services.table_generator import (
    build_table,
    render_page,
    _parse_upload,
)
from services.plot_generator import build_plot_html
from utils.data_loader import load_data

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


@route("/generate_table", method="POST")
def generate_table_route():
    mode = request.forms.getunicode("mode", "generate")
    upload_file = request.files.get("csv_file")

    rows = int(request.forms.get("rows") or 100)
    cols = int(request.forms.get("cols") or 5)
    pattern = request.forms.getunicode("pattern", "linear")

    table_html, error_html = build_table(
        mode=mode,
        upload_file=upload_file,
        rows=rows,
        cols=cols,
        pattern=pattern,
    )

    response.content_type = "text/html; charset=utf-8"
    return render_page(table_html, error_html)

@route("/generate_plots", method="POST")
def generate_plots_route() -> str:
    mode = request.forms.getunicode("mode", "generate")
    upload_file = request.files.get("csv_file")

    rows = int(request.forms.get("rows") or 100)
    cols = int(request.forms.get("cols") or 5)
    pattern = request.forms.getunicode("pattern", "linear")

    plot_type = request.forms.getunicode("plot_type", "hist")

    try:
        if mode == "upload":
            df = _parse_upload(upload_file)
        else:
            df = load_data(rows=rows, cols=cols, pattern=pattern)

        html_snippet = build_plot_html(plot_type, df)
        error_html: Optional[str] = None
    except Exception as exc:
        html_snippet = None
        error_html = f"<div class='alert alert-danger'>{exc}</div>"

    response.content_type = "text/html; charset=utf-8"
    return render_page(html_snippet, error_html)


@route('/variant1', method='GET')
@view('variant1')
def variant1_page():
    """Рендер страницы для первого варианта."""
    return dict(year=datetime.now().year)

@route('/variant2')
@view('variant2')
def about():
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