import os
from datetime import datetime
from io import BytesIO
from uuid import uuid4

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from bottle import view
from utils.data_loader import load_data


@view('variant2')
def render_variant2_template():
    """Обработка GET-запроса: просто вернуть пустую форму."""
    return dict(
        year=datetime.now().year,
        table=None,
        error=None,
        corr_matrix=None,
        heatmap_url=None,
    )


@view('variant2')
def process_variant2_post(request):
    """Обработка POST-запроса: создать таблицу, корреляцию и тепловую карту."""
    table_html = None
    error = None
    corr_matrix_html = None
    heatmap_filename = None

    try:
        mode = request.forms.getunicode('mode', 'generate')
        upload = request.files.get('csv_file')

        # ---------- Загруженный файл ----------
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
                raise ValueError('Поддерживаются только CSV, TSV или JSON.')
            df = parser_map[ext](raw)

        # ---------- Синтетические данные ----------
        else:
            rows = int(request.forms.get('rows') or 100)
            cols = int(request.forms.get('cols') or 5)
            pattern = request.forms.getunicode('pattern', 'linear')
            df = load_data(rows=rows, cols=cols, pattern=pattern)

        # ---------- Таблица ----------
        table_html = df.to_html(
            classes='table table-striped table-bordered',
            index=False,
            border=0,
            max_rows=None,
            max_cols=None,
        )

        # ---------- Корреляция ----------
        corr = df.corr(numeric_only=True)
        corr_matrix_html = corr.to_html(classes='table table-bordered', border=0)

        # ---------- Тепловая карта ----------
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True, ax=ax)
        plt.title("Тепловая карта корреляции", fontsize=16)
        plt.tight_layout()

        heatmap_filename = f"heatmap_{uuid4().hex[:8]}.png"
        heatmap_path = os.path.join("static", heatmap_filename)
        plt.savefig(heatmap_path)
        plt.close()

    except Exception as exc:
        error = str(exc)

    return dict(
        year=datetime.now().year,
        table=table_html,
        error=error,
        corr_matrix=corr_matrix_html,
        heatmap_url=heatmap_filename,
    )
