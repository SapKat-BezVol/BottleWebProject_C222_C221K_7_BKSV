from __future__ import annotations
import pathlib
from typing import Literal
import numpy as np
import pandas as pd

__all__ = [
    "load_data",
    "generate_synthetic",
    "get_preview",
]

def load_data(
    source: str | pathlib.Path | None = None,
    *,
    rows: int | None = None,
    cols: int | None = None,
    pattern: Literal["linear", "sin", "random"] = "linear",
    seed: int = 1488,
) -> pd.DataFrame:
    if source is not None:
        path = pathlib.Path(source).expanduser()
        if not path.exists():
            raise FileNotFoundError(f"Data file {path} does not exist.")

        suffix = path.suffix.lower()
        if suffix == ".csv":
            return pd.read_csv(path)
        if suffix == ".tsv":
            return pd.read_csv(path, sep="\t")
        if suffix == ".json":
            return pd.read_json(path)
        raise ValueError(f"Unsupported file extension: {suffix}")

    return generate_synthetic(rows=rows, cols=cols, pattern=pattern, seed=seed)


def generate_synthetic(
    *,
    rows: int | None = None,
    cols: int | None = None,
    pattern: Literal["linear", "sin", "random"] = "linear",
    seed: int = 1488,
) -> pd.DataFrame:
    """Generate deterministic synthetic numeric data."""

    rows = max(1, min(int(rows or 1000), 1000))
    cols = max(1, min(int(cols or 5), 10))

    rng = np.random.default_rng(seed)
    index = np.arange(rows)

    if pattern == "linear":
        data = np.vstack([(j + 1) * (index + 1) for j in range(cols)]).T
    elif pattern == "sin":
        data = np.vstack([
            np.sin(2 * np.pi * (index + 1) / (j + 1)) for j in range(cols)
        ]).T
    elif pattern == "random":
        data = rng.random((rows, cols))
    else:
        raise ValueError(f"Unknown pattern '{pattern}'")

    columns = [f"col_{j+1}" for j in range(cols)]
    return pd.DataFrame(data, columns=columns)


def get_preview(
    df: pd.DataFrame,
    *,
    method: Literal["head", "tail", "sample"] = "head",
    n: int = 10,
    seed: int = 1488,
) -> pd.DataFrame:
    """Return a lightweight preview of *df* without altering the original."""

    if n <= 0:
        raise ValueError("n must be positive")

    if method == "head":
        return df.head(n)
    if method == "tail":
        return df.tail(n)
    if method == "sample":
        return df.sample(n=min(n, len(df)), random_state=seed)

    raise ValueError(f"Unknown preview method '{method}'")
