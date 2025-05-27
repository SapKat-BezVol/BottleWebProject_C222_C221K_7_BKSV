from __future__ import annotations
import pathlib
import random
from typing import Literal
import numpy as np
import pandas as pd

__all__ = ["load_data", "generate_synthetic", "get_preview"]

# ──────────────────────────────────────────────────────────────────────────────
PatternStr = Literal["linear", "gaussian", "sine"]

# ──────────────────────────────────────────────────────────────────────────────
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
    return generate_synthetic(rows=rows, cols=cols, pattern=pattern)

def _generate_linear(rows: int, cols: int, rng: np.random.Generator) -> pd.DataFrame:
    idx = np.arange(rows)
    data = np.empty((rows, cols))
    for c in range(cols):
        start = rng.uniform(-100, 100)
        step = rng.uniform(-10, 10)
        data[:, c] = start + step * idx
    return pd.DataFrame(data, columns=[f"col_{i + 1}" for i in range(cols)])

def _generate_sine(rows: int, cols: int, rng: np.random.Generator) -> pd.DataFrame:
    idx = np.arange(rows)
    data = np.empty((rows, cols))
    for c in range(cols):
        amplitude = rng.uniform(0.5, 5.0)
        cycles = rng.uniform(0.25, 4.0)
        frequency = 2.0 * np.pi * cycles / rows
        phase = rng.uniform(0, 2.0 * np.pi)
        data[:, c] = amplitude * np.sin(frequency * idx + phase)
    return pd.DataFrame(data, columns=[f"col_{i + 1}" for i in range(cols)])

def _generate_gaussian(rows: int, cols: int, rng: np.random.Generator) -> pd.DataFrame:
    data = rng.normal(loc=0.0, scale=1.0, size=(rows, cols))
    return pd.DataFrame(data, columns=[f"col_{i + 1}" for i in range(cols)])

def generate_synthetic(
    *,
    rows: int | None = None,
    cols: int | None = None,
    pattern: PatternStr = "linear",
) -> pd.DataFrame:
    """
    Создать таблицу по паттерну с каждый раз разными значениями.
    Patterns:
    - linear: (j+1)*(i+1)+noise
    - sine: sin(2π*(i+1)/(j+1))+noise
    - gaussian: N(0,1)
    """
    # Валидация размерностей
    if rows is not None and rows < 0:
        raise ValueError("rows must be non-negative")
    if cols is not None and cols < 0:
        raise ValueError("cols must be non-negative")
    rows = max(1, min(int(rows or 1000), 1000))
    cols = max(1, min(int(cols or 5), 10))

    rng = np.random.default_rng()
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
    """Вернуть небольшой срез *df*, не изменяя оригинал."""
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
