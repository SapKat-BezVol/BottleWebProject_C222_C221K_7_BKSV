from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from bottle import request

def build_prediction_numbers(df: pd.DataFrame) -> str:
    """Возвращает предсказанные числа"""
    try:
        # Получаем параметры из формы
        target_col_num = int(request.forms.get('target_col')) - 1
        features_input = request.forms.get('features')
        
        # Проверяем корректность ввода
        if target_col_num < 0 or target_col_num >= len(df.columns):
            raise ValueError("Некорректный номер целевого столбца")
            
        target_col = df.columns[target_col_num]
        X = df.drop(columns=[target_col])
        y = df[target_col]
        
        # Преобразуем введенные данные
        features = [float(x) for x in features_input.split()]
        if len(features) != len(X.columns):
            raise ValueError(f"Ожидается {len(X.columns)} признаков, получено {len(features)}")
            
        new_data = np.array(features).reshape(1, -1)
        
        # Строим модель и делаем предсказание
        model = LinearRegression()
        model.fit(X, y)
        prediction = model.predict(new_data)[0]
        
        # Формируем результат
        result = f"""
        <div class="alert alert-success">
            <h4>Результат предсказания</h4>
            <p><strong>Целевая переменная:</strong> {target_col}</p>
            <p><strong>Введенные признаки:</strong> {', '.join(f'{col}: {val:.2f}' for col, val in zip(X.columns, features))}</p>
            <p><strong>Прогнозируемое значение:</strong> {prediction:.4f}</p>
        </div>
        """
        
        return result
        
    except Exception as e:
        return f"<div class='alert alert-danger'>Ошибка: {str(e)}</div>"
