"""Tests for the feature-processing functions.

CI runs these on every push and pull request. If a test fails, the red X on
GitHub tells you *before* a collaborator (or you) builds on broken code.
"""

import numpy as np
import pandas as pd
import pytest

from rnaseq_tutorial.data import simulate_counts
from rnaseq_tutorial.features import filter_low_counts, log_transform, normalize_cpm
from rnaseq_tutorial.model import differential_expression


@pytest.fixture
def counts():
    """A small reproducible count matrix shared across tests."""
    mat, _ = simulate_counts(n_genes=200, n_per_group=4, n_de_genes=20, seed=42)
    return mat


def test_filter_low_counts_removes_low_genes(counts):
    counts.iloc[0] = 0  # force a gene with zero total
    filtered = filter_low_counts(counts, min_total=10)
    assert counts.index[0] not in filtered.index
    assert (filtered.sum(axis=1) >= 10).all()


def test_normalize_cpm_columns_sum_to_one_million(counts):
    cpm = normalize_cpm(counts)
    np.testing.assert_allclose(cpm.sum(axis=0), 1e6, rtol=1e-6)


def test_log_transform_handles_zeros():
    df = pd.DataFrame({"a": [0.0, 1.0, 3.0]})
    result = log_transform(df, pseudocount=1.0)
    assert np.isfinite(result.to_numpy()).all()
    assert result.iloc[0, 0] == 0.0  # log2(0 + 1) == 0


def test_differential_expression_recovers_known_de_genes():
    """The first 30 genes are simulated as DE — most should be flagged significant."""
    counts, labels = simulate_counts(n_genes=500, n_per_group=8, n_de_genes=30, seed=1)
    results = differential_expression(counts, labels)
    true_de = {f"GENE{i:04d}" for i in range(30)}
    detected = set(results.index[results["significant"]])
    recall = len(true_de & detected) / len(true_de)
    assert recall > 0.5  # we should recover the majority of true signals
