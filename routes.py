from datetime import datetime
from io import BytesIO
from bottle import route, view, request, response
from services.table_generator import build_table, render_page
import pandas as pd


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