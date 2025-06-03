"""
Модуль предоставляет функции для загрузки готовых таблиц из файлов CSV/TSV/JSON
или для синтетической генерации числовых данных по трём базовым паттернам
(`linear`, `sine`, `gaussian`). Также содержит утилиту для просмотра
небольшого среза (превью) произвольного DataFrame.
"""

from __future__ import annotations

import pathlib
import random
from typing import Literal, Optional

import numpy as np
import pandas as pd

__all__ = [
    "load_data",
    "generate_synthetic",
    "get_preview",
]

# ---------------------------------------------------------------------------
# Типы и константы
# ---------------------------------------------------------------------------
PatternStr = Literal["linear", "gaussian", "sine"]


# ---------------------------------------------------------------------------
# Публичные API
# ---------------------------------------------------------------------------

def load_data(
    source: str | pathlib.Path | None = None,
    *,
    rows: int | None = None,
    cols: int | None = None,
    pattern: PatternStr = "linear",
    seed: int | None = None,
) -> pd.DataFrame:
    """Загрузить данные из файла или сгенерировать синтетические.

    Если указан *source*, функция пытается прочитать файл. Поддерживаются
    форматы CSV (`.csv`), TSV (`.tsv`) и JSON (`.json`). Любой другой
    расширение вызывает исключение :class:`ValueError`.

    Если *source* равен ``None``, вызывается
    :func:`generate_synthetic` с указанными параметрами.

    Параметры
    ----------
    source : str | pathlib.Path | None, optional
        Путь к файлу‑источнику. Если ``None`` – данные генерируются.
    rows : int | None, optional
        Число строк для синтетической генерации (ограничение 1 … 1000).
    cols : int | None, optional
        Число столбцов для синтетической генерации (ограничение 1 … 10).
    pattern : {"linear", "gaussian", "sine"}, default "linear"
        Паттерн генерации (см. :func:`generate_synthetic`).
    seed : int | None, optional
        Значение для инициализации ГПСЧ NumPy.

    Возвращает
    ---------
    pandas.DataFrame
        Загрузанный или синтетический датафрейм.

    Исключения
    ----------
    FileNotFoundError
        Файл не найден или не является обычным файлом.
    ValueError
        Неподдерживаемое расширение файла.
    """
    if source is not None:
        path = pathlib.Path(source).expanduser()
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"File {path} not found.")

        # Сопоставление расширения файла с корректным ридером pandas
        match path.suffix.lower():
            case ".csv":
                return pd.read_csv(path)
            case ".tsv":
                return pd.read_csv(path, sep="\t")
            case ".json":
                return pd.read_json(path)
            case _:
                raise ValueError(f"Unsupported extension: {path.suffix}")

    # Файл не указан – генерируем данные
    return generate_synthetic(rows=rows, cols=cols, pattern=pattern, seed=seed)


# ---------------------------------------------------------------------------
# Внутренние генераторы
# ---------------------------------------------------------------------------

def _generate_linear(rows: int, cols: int, rng: np.random.Generator) -> pd.DataFrame:
    """Сгенерировать матрицу линейного паттерна с гауссовским шумом.

    Ячейки вычисляются по формуле ``(i + 1) * (j + 1)`` с добавлением
    случайного шума *N(0, σ²)*, где σ выбирается случайным образом в
    диапазоне ``[0, 10]``.
    """
    i = np.arange(rows)[:, None]
    j = np.arange(1, cols + 1)[None, :]
    base = (i + 1) * j

    noise_scale = rng.uniform(0.0, 10.0)
    noise = rng.normal(loc=0.0, scale=noise_scale, size=(rows, cols))

    data = base + noise
    return pd.DataFrame(data, columns=[f"col_{k}" for k in range(1, cols + 1)])


def _generate_sine(
    rows: int,
    cols: int,
    rng: np.random.Generator,
    noise_scale: Optional[float] = None,
) -> pd.DataFrame:
    """Сгенерировать синусоидальный паттерн с добавлением шума.

    Для каждого столбца выбирается индивидуальная амплитуда, число циклов и
    фазовый сдвиг. Итоговая синусоида искажается аддитивным гауссовским
    шумом, масштаб которого пропорционален амплитуде.
    """
    idx = np.arange(rows)
    data = np.empty((rows, cols), dtype=float)

    if noise_scale is None:
        # Шкала шума по умолчанию — небольшая доля амплитуды
        noise_scale = rng.uniform(0.0, 0.10)

    for c in range(cols):
        # Параметры синусоиды выбираются случайно для каждого столбца
        amplitude = rng.uniform(0.5, 5.0)
        cycles = rng.uniform(0.25, 4.0)
        freq = 2.0 * np.pi * cycles / rows
        phase = rng.uniform(0, 2.0 * np.pi)

        clean = amplitude * np.sin(freq * idx + phase)
        noise = rng.normal(loc=0.0, scale=noise_scale * amplitude, size=rows)

        data[:, c] = clean + noise

    col_names = [f"col_{i + 1}" for i in range(cols)]
    return pd.DataFrame(data, columns=col_names)


def _generate_gaussian(rows: int, cols: int, rng: np.random.Generator) -> pd.DataFrame:
    """Сгенерировать таблицу чистого гауссовского шума *N(0, 1.5²).*"""
    noise_scale = 1.5
    data = rng.normal(loc=0.0, scale=noise_scale, size=(rows, cols))
    return pd.DataFrame(data, columns=[f"col_{k}" for k in range(1, cols + 1)])


# ---------------------------------------------------------------------------
# Публичная генерация данных
# ---------------------------------------------------------------------------

def generate_synthetic(
    *,
    rows: int | None = None,
    cols: int | None = None,
    pattern: PatternStr = "linear",
    seed: int | None = None,
) -> pd.DataFrame:
    """Сгенерировать DataFrame по указанному паттерну.

    Поддерживаемые паттерны:
    * ``linear``   – (i + 1)*(j + 1) + *N(0, σ²)*, σ ∈ [0 … 10]
    * ``sine``     – синусоида с параметрами, зависящими от столбца, + шум
    * ``gaussian`` – чистый гауссов шум *N(0, 1.5²)*

    Число строк и столбцов ограничено диапазонами 1 … 1000 и 1 … 10
    соответственно.
    """
    if rows is not None and rows < 0:
        raise ValueError("rows must be non-negative")
    if cols is not None and cols < 0:
        raise ValueError("cols must be non-negative")

    rows = max(1, min(int(rows or 1000), 1000))
    cols = max(1, min(int(cols or 5), 10))

    rng = np.random.default_rng(seed)

    pat = pattern.lower()
    if pat == "linear":
        return _generate_linear(rows, cols, rng)
    if pat == "sine":
        return _generate_sine(rows, cols, rng)
    if pat == "gaussian":
        return _generate_gaussian(rows, cols, rng)

    raise ValueError(f"Unknown pattern '{pattern}'")


# ---------------------------------------------------------------------------
# Просмотр данных
# ---------------------------------------------------------------------------

def get_preview(
    df: pd.DataFrame,
    *,
    method: Literal["head", "tail", "sample"] = "head",
    n: int = 10,
    seed: int | None = None,
) -> pd.DataFrame:
    """Вернуть небольшой срез *df*, не изменяя сам объект.

    Параметры
    ----------
    df : pandas.DataFrame
        Источник данных для превью.
    method : {"head", "tail", "sample"}, default "head"
        Способ формирования выборки:
        * ``head``   – первые *n* строк;
        * ``tail``   – последние *n* строк;
        * ``sample`` – случайные *n* строк.
    n : int, default 10
        Число строк в выборке (> 0).
    seed : int | None, optional
        Инициализация ГПСЧ для метода ``sample``.

    Возвращает
    ---------
    pandas.DataFrame
        Новый датафрейм‑выборка той же структуры, что и исходный.

    Исключения
    ----------
    ValueError
        *n* ≤ 0 или неизвестное значение *method*.
    """
    if n <= 0:
        raise ValueError("n must be positive")

    if method == "head":
        return df.head(n)
    if method == "tail":
        return df.tail(n)
    if method == "sample":
        random_state = seed if seed is not None else random.randint(0, 2**32 - 1)
        return df.sample(n=min(n, len(df)), random_state=random_state)

    raise ValueError(f"Unknown preview method '{method}'")
