"""Differential expression testing.

A deliberately simple per-gene t-test with multiple-testing correction. Real
pipelines use DESeq2/edgeR/limma, but the *interface* — counts in, ranked
results out — is what matters for the tutorial.
"""

from __future__ import annotations

import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

from rnaseq_tutorial.features import filter_low_counts, log_transform, normalize_cpm


def differential_expression(
    counts: pd.DataFrame,
    labels: pd.Series,
    group_a: str = "control",
    group_b: str = "treatment",
    alpha: float = 0.05,
) -> pd.DataFrame:
    """Run a per-gene two-sample t-test between two groups.

    Returns a results table sorted by adjusted p-value, with columns:
    ``log2_fold_change``, ``p_value``, ``p_adj`` (Benjamini-Hochberg), ``significant``.
    """
    counts = filter_low_counts(counts)
    logcpm = log_transform(normalize_cpm(counts))

    samples_a = labels.index[labels == group_a]
    samples_b = labels.index[labels == group_b]
    mat_a = logcpm[samples_a]
    mat_b = logcpm[samples_b]

    t_stat, p_value = stats.ttest_ind(mat_b, mat_a, axis=1)
    log2fc = mat_b.mean(axis=1) - mat_a.mean(axis=1)

    reject, p_adj, _, _ = multipletests(p_value, alpha=alpha, method="fdr_bh")

    results = pd.DataFrame(
        {
            "log2_fold_change": log2fc.to_numpy(),
            "p_value": p_value,
            "p_adj": p_adj,
            "significant": reject,
        },
        index=counts.index,
    )
    return results.sort_values("p_adj")
