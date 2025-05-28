from __future__ import annotations
import base64
import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def _fig_to_base64(fig: plt.Figure) -> str:
    """Конвертирует matplotlib figure в base64 строку."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('ascii')

def analyze_distributions(df: pd.DataFrame) -> dict:
    """
    Анализирует распределения всех числовых столбцов.
    Возвращает словарь с результатами анализа и графиками.
    """
    results = {}
    
    for col in df.select_dtypes(include=['number']).columns:
        col_data = df[col].dropna()
        if len(col_data) < 2:
            continue
            
        # Статистические характеристики
        stats_dict = {
            'mean': col_data.mean(),
            'median': col_data.median(),
            'std': col_data.std(),
            'skewness': col_data.skew(),
            'kurtosis': col_data.kurtosis(),
            'shapiro_p': stats.shapiro(col_data)[1] if len(col_data) <= 5000 else None
        }
        
        # Проверка на нормальность
        is_normal = False
        if stats_dict['shapiro_p'] is not None:
            is_normal = stats_dict['shapiro_p'] > 0.05
        stats_dict['is_normal'] = is_normal
        
        # Поиск выбросов (метод IQR)
        q1 = col_data.quantile(0.25)
        q3 = col_data.quantile(0.75)
        iqr = q3 - q1
        outliers = col_data[(col_data < (q1 - 1.5*iqr)) | (col_data > (q3 + 1.5*iqr))]
        stats_dict['outliers_count'] = len(outliers)
        stats_dict['outliers_percent'] = len(outliers)/len(col_data)*100
        
        # Гистограмма с KDE
        plt.figure(figsize=(10, 6))
        sns.histplot(col_data, kde=True, stat='density')
        plt.title(f'Распределение {col}')
        if is_normal:
            plt.axvline(stats_dict['mean'], color='r', linestyle='--', label='Mean')
            x = np.linspace(col_data.min(), col_data.max(), 100)
            plt.plot(x, stats.norm.pdf(x, stats_dict['mean'], stats_dict['std']), 
                    'r-', lw=2, label='Normal dist')
        plt.legend()
        plot_b64 = _fig_to_base64(plt.gcf())
        plt.close()
        
        results[col] = {
            'stats': stats_dict,
            'plot': plot_b64
        }
    
    return results

def generate_distribution_html(df: pd.DataFrame) -> str:
    """Генерирует HTML с анализом распределений."""
    analysis = analyze_distributions(df)
    
    if not analysis:
        return "<div class='alert alert-warning'>Нет числовых столбцов для анализа</div>"
    
    html_parts = []
    for col, data in analysis.items():
        stats = data['stats']
        
        # Блок статистики
        stats_html = f"""
        <div class='card mb-4'>
            <div class='card-header'>
                <h4>Столбец: {col}</h4>
            </div>
            <div class='card-body'>
                <div class='row'>
                    <div class='col-md-6'>
                        <img class='img-fluid' src='data:image/png;base64,{data["plot"]}'>
                    </div>
                    <div class='col-md-6'>
                        <table class='table table-bordered'>
                            <tr><th>Характеристика</th><th>Значение</th></tr>
                            <tr><td>Среднее</td><td>{stats['mean']:.4f}</td></tr>
                            <tr><td>Медиана</td><td>{stats['median']:.4f}</td></tr>
                            <tr><td>Станд. отклонение</td><td>{stats['std']:.4f}</td></tr>
                            <tr><td>Асимметрия</td><td>{stats['skewness']:.4f}</td></tr>
                            <tr><td>Эксцесс</td><td>{stats['kurtosis']:.4f}</td></tr>
                            <tr><td>Нормальное распределение?</td>
                                <td>{'Да' if stats['is_normal'] else 'Нет'}</td></tr>
                            <tr><td>Количество выбросов</td><td>{stats['outliers_count']}</td></tr>
                            <tr><td>Процент выбросов</td><td>{stats['outliers_percent']:.2f}%</td></tr>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        """
        html_parts.append(stats_html)
    
    return "\n".join(html_parts)