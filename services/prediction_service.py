from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def train_model(df: pd.DataFrame) -> tuple[LinearRegression, str]:
    """Обучает модель и возвращает её вместе с именем целевой переменной"""
    target_col = df.columns[-1]
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    model = LinearRegression()
    model.fit(X, y)
    return model, target_col

def make_prediction(model: LinearRegression, features: list[float]) -> float:
    """Делает предсказание на основе обученной модели"""
    return model.predict([features])[0]

def prepare_demo_data() -> pd.DataFrame:
    """Создает демо-датафрейм если нет загруженных данных"""
    data = np.random.rand(100, 3) * 100
    return pd.DataFrame(data, columns=[f'Признак_{i+1}' for i in range(3)])