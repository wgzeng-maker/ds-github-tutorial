"""Feature processing: filtering and normalization.

Small, pure functions with type hints and docstrings. Each does one thing,
which is exactly what makes them easy to test in tests/test_features.py.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def filter_low_counts(counts: pd.DataFrame, min_total: int = 10) -> pd.DataFrame:
    """Drop genes whose total count across all samples is below ``min_total``.

    Low-count genes are noisy and inflate multiple-testing burden, so filtering
    them is standard practice before differential expression.
    """
    keep = counts.sum(axis=1) >= min_total
    return counts.loc[keep]


def normalize_cpm(counts: pd.DataFrame) -> pd.DataFrame:
    """Counts-per-million normalization to correct for library size differences.

    CPM_{gene,sample} = counts / (library size) * 1e6
    """
    library_size = counts.sum(axis=0)
    return counts.div(library_size, axis=1) * 1e6


def log_transform(values: pd.DataFrame, pseudocount: float = 1.0) -> pd.DataFrame:
    """log2(x + pseudocount). The pseudocount avoids log(0)."""
    return np.log2(values + pseudocount)
