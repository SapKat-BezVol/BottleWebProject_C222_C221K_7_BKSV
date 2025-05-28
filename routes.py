from __future__ import annotations

from datetime import datetime
from io import BytesIO
from bottle import route, template, view, request, response
import pandas as pd
from services.correlation_generator import build_correlation_table,build_correlation_heatmap
from services.table_generator import build_table, _parse_upload, render_page, load_data
from services.plot_generator import build_plot_html
import numpy as np
from sklearn.linear_model import LinearRegression
from services.prediction_service import train_model, make_prediction, prepare_demo_data

# Глобальная переменная
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


@route('/generate_table', method='POST')
def generate_table():
    global generated_df
    try:
        mode = request.forms.get('mode')

        if mode == 'upload':
            upload_file = request.files.get('csv_file')
            html_table, error_html, df = build_table(mode, upload_file)
        else:
            rows = int(request.forms.get('rows', 100))
            cols = int(request.forms.get('cols', 5))
            pattern = request.forms.get('pattern', 'linear')
            html_table, error_html, df = build_table(mode, None, rows, cols, pattern)

        if error_html:
            return error_html
        print("DEBUG build_table df.head():")
        print(df.head())

        print("DEBUG build_table df.describe():")
        print(df.describe())

        generated_df = df
        return html_table

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"<p class='text-danger'>Внутренняя ошибка сервера: {e}</p>"



@route("/generate_correlation", method="POST")
def generate_correlation_route() -> str:
    global generated_df
    if generated_df is None:
        error_html = "<div class='alert alert-danger'>Сначала сгенерируйте или загрузите таблицу</div>"
        return render_page("", error_html)

    try:
        table_html = build_correlation_table(generated_df)
        heatmap_html = build_correlation_heatmap(generated_df)
        combined_html = table_html + heatmap_html
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


@route('/predict', method=['GET', 'POST'])
@view('predict')
def predict_page():
    """Рендер страницы предсказания"""
    global generated_df
    if generated_df is None:
        # Если данных нет, создаем демо-датафрейм
        data = np.random.rand(100, 3) * 100
        generated_df = pd.DataFrame(data, columns=[f'Признак_{i+1}' for i in range(3)])
    
    return dict(
        year=datetime.now().year,
        num_features=len(generated_df.columns)-1
    )

@route("/make_prediction", method="POST")
def make_prediction() -> str:
    global generated_df
    if generated_df is None:
        error_html = "<div class='alert alert-danger'>Сначала сгенерируйте или загрузите таблицу</div>"
        return render_page("", error_html)
    
    try:
        # Получаем данные из формы
        features = []
        for i in range(len(generated_df.columns)-1):
            val = request.forms.get(f"feature_{i}")
            features.append(float(val))
        
        # Делаем предсказание
        target_col = generated_df.columns[-1]
        X = generated_df.drop(columns=[target_col])
        y = generated_df[target_col]
        
        model = LinearRegression()
        model.fit(X, y)
        
        prediction = model.predict([features])[0]
        
        # Формируем HTML с результатами
        html_snippet = f"""
        <div class="alert alert-success mt-3">
            <h4>Результат предсказания</h4>
            <p>Для признаков: {', '.join(map(str, features))}</p>
            <p>Прогнозируемое значение '{target_col}': <strong>{prediction:.2f}</strong></p>
        </div>
        """
        error_html = None
    except Exception as exc:
        html_snippet = ""
        error_html = f"<div class='alert alert-danger'>Ошибка: {exc}</div>"
    
    response.content_type = "text/html; charset=utf-8"
    return render_page(html_snippet, error_html)


@route('/variant1', method='GET')
@view('variant1')
def variant1_page():
    """Рендер страницы для первого варианта."""
    return dict(year=datetime.now().year)

@route('/variant2', method=['GET', 'POST'])
@view('variant2')
def variant2():
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