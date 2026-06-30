"""Data loading and simulation.

Keep I/O separate from analysis. Functions that *read* data should not also
*transform* it — that separation makes each piece independently testable.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def simulate_counts(
    n_genes: int = 1000,
    n_per_group: int = 6,
    n_de_genes: int = 100,
    seed: int = 0,
) -> tuple[pd.DataFrame, pd.Series]:
    """Simulate a small RNA-seq count matrix with known differentially-expressed genes.

    Using a fixed ``seed`` makes the toy data reproducible — a recurring theme in
    this repo. Real projects download real data, but the principle is identical:
    the result must be regenerable.

    Returns:
        counts: genes (rows) x samples (columns) integer count matrix.
        labels: sample -> group ("control" / "treatment").
    """
    rng = np.random.default_rng(seed)
    samples = [f"ctrl_{i}" for i in range(n_per_group)] + [
        f"trt_{i}" for i in range(n_per_group)
    ]
    labels = pd.Series(
        ["control"] * n_per_group + ["treatment"] * n_per_group, index=samples, name="group"
    )

    base_mean = rng.uniform(5, 500, size=n_genes)
    counts = np.zeros((n_genes, len(samples)), dtype=int)
    for j, group in enumerate(labels):
        means = base_mean.copy()
        if group == "treatment":
            # The first n_de_genes are truly differentially expressed.
            fold = rng.uniform(2, 5, size=n_de_genes)
            means[:n_de_genes] *= fold
        counts[:, j] = rng.poisson(means)

    gene_ids = [f"GENE{i:04d}" for i in range(n_genes)]
    return pd.DataFrame(counts, index=gene_ids, columns=samples), labels


def load_counts(path: str | Path) -> pd.DataFrame:
    """Load a counts matrix from a CSV (genes as rows, samples as columns)."""
    return pd.read_csv(path, index_col=0)
