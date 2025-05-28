from __future__ import annotations
import pathlib
import random
from typing import Literal, Optional
import numpy as np
import pandas as pd

__all__ = ["load_data", "generate_synthetic", "get_preview"]

PatternStr = Literal["linear", "gaussian", "sine"]

def load_data(
    source: str | pathlib.Path | None = None,
    *,
    rows: int | None = None,
    cols: int | None = None,
    pattern: PatternStr = "linear",
    seed: int | None = None,
) -> pd.DataFrame:
    if source is not None:
        path = pathlib.Path(source).expanduser()
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"File {path} not found.")
        match path.suffix.lower():
            case ".csv":
                return pd.read_csv(path)
            case ".tsv":
                return pd.read_csv(path, sep="\t")
            case ".json":
                return pd.read_json(path)
            case _:
                raise ValueError(f"Unsupported extension: {path.suffix}")
    return generate_synthetic(rows=rows, cols=cols, pattern=pattern, seed=seed)


def _generate_linear(rows: int, cols: int, rng: np.random.Generator) -> pd.DataFrame:
    """
    Линейная матрица: (i+1)*(j+1) с аддитивным гауссовским шумом.
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
    noise_scale: Optional[float] = None
) -> pd.DataFrame:
    idx = np.arange(rows)
    data = np.empty((rows, cols), dtype=float)
    if noise_scale is None:
        noise_scale = rng.uniform(0.0, 0.10)
    for c in range(cols):
        # базовые параметры синусоиды
        amplitude = rng.uniform(0.5, 5.0)
        cycles    = rng.uniform(0.25, 4.0)
        freq      = 2.0 * np.pi * cycles / rows
        phase     = rng.uniform(0, 2.0 * np.pi)

        # чистая синусоида
        clean = amplitude * np.sin(freq * idx + phase)
        # шум: нормальное распределение с σ = noise_scale * amplitude
        noise = rng.normal(loc=0.0, scale=noise_scale * amplitude, size=rows)

        data[:, c] = clean + noise

    cols_names = [f"col_{i+1}" for i in range(cols)]
    return pd.DataFrame(data, columns=cols_names)

def _generate_gaussian(rows: int, cols: int, rng: np.random.Generator) -> pd.DataFrame:
    """
    Гауссовский шум: N(0, scale) с оптимизированной дисперсией.
    """
    noise_scale = 1.5
    data = rng.normal(loc=0.0, scale=noise_scale, size=(rows, cols))
    return pd.DataFrame(data, columns=[f"col_{k}" for k in range(1, cols + 1)])


def generate_synthetic(
    *,
    rows: int | None = None,
    cols: int | None = None,
    pattern: PatternStr = "linear",
    seed: int | None = None,
) -> pd.DataFrame:
    """
    Создать таблицу по паттерну с оптимизированным постоянным шумом.
    Patterns:
    - linear: (i+1)*(j+1) + N(0,2.0)
    - sine: 2*sin(2π*i/rows + φ) + N(0,0.2)
    - gaussian: N(0,1.5)
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
    elif pat == "sine":
        return _generate_sine(rows, cols, rng)
    elif pat == "gaussian":
        return _generate_gaussian(rows, cols, rng)
    else:
        raise ValueError(f"Unknown pattern '{pattern}'")


def get_preview(
    df: pd.DataFrame,
    *,
    method: Literal["head", "tail", "sample"] = "head",
    n: int = 10,
    seed: int | None = None,
) -> pd.DataFrame:
    """Вернуть небольшой срез df, не изменяя оригинал."""
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
