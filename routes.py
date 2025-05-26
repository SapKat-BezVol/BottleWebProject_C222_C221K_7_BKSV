from datetime import datetime
from io import BytesIO
from bottle import route, view, request
from utils.data_loader import load_data, get_preview
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

@route('/variant1', method=['GET', 'POST'])
@view('variant1')
def variant1():
    table_html: str | None = None
    error: str | None = None

    if request.method == 'POST':
        try:
            mode = request.forms.getunicode('mode', 'generate')
            upload = request.files.get('csv_file')

            # ----------------------------- upload mode ---------------------
            if mode == 'upload':
                if not (upload and upload.filename):
                    raise ValueError('Файл не выбран.')

                ext = upload.filename.rsplit('.', 1)[-1].lower()
                raw = upload.file.read()
                parser_map = {
                    'csv': lambda b: pd.read_csv(BytesIO(b)),
                    'tsv': lambda b: pd.read_csv(BytesIO(b), sep='\t'),
                    'json': lambda b: pd.read_json(BytesIO(b)),
                }
                if ext not in parser_map:
                    raise ValueError('Поддерживаются файлы CSV, TSV или JSON.')
                df = parser_map[ext](raw)

            # -------------------------- synthetic mode --------------------
            else:  # default «generate»
                rows = int(request.forms.get('rows') or 100)
                cols = int(request.forms.get('cols') or 5)
                pattern = request.forms.getunicode('pattern', 'linear')

                if not 1 <= rows <= 1000:
                    raise ValueError('Количество строк должно быть от 1 до 1000.')
                if not 1 <= cols <= 10:
                    raise ValueError('Количество столбцов должно быть от 1 до 10.')

                df = load_data(rows=rows, cols=cols, pattern=pattern)

            # ----------------------------- render full table --------------
            table_html = df.to_html(
                classes='table table-striped table-bordered',
                index=False,
                border=0,
                max_rows=None,
                max_cols=None,
            )

        except Exception as exc:
            error = str(exc)

    return dict(
        year=datetime.now().year,
        table=table_html,
        error=error,
    )

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