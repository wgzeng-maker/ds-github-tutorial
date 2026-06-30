"""Plotting helpers.

Design note: the *computation* (what to plot) is separated from the *drawing*
(matplotlib). ``volcano_data`` is pure and testable; ``volcano_plot`` only draws.
This keeps the testable logic free of a hard matplotlib dependency.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def volcano_data(
    results: pd.DataFrame,
    lfc_threshold: float = 1.0,
    alpha: float = 0.05,
) -> pd.DataFrame:
    """Compute volcano-plot coordinates from a differential-expression table.

    A volcano plot shows effect size (x = log2 fold change) against significance
    (y = -log10 p-value), so the most interesting genes — large change *and* highly
    significant — sit in the top corners.

    Expects the columns produced by ``model.differential_expression``:
    ``log2_fold_change``, ``p_value``, ``p_adj``.

    Returns the input frame plus ``neg_log10_p`` and a ``category`` label of
    "up", "down", or "ns" (not significant).
    """
    out = results.copy()
    out["neg_log10_p"] = -np.log10(out["p_value"].clip(lower=1e-300))

    sig = out["p_adj"] < alpha
    up = sig & (out["log2_fold_change"] >= lfc_threshold)
    down = sig & (out["log2_fold_change"] <= -lfc_threshold)

    out["category"] = "ns"
    out.loc[up, "category"] = "up"
    out.loc[down, "category"] = "down"
    return out


def volcano_plot(results: pd.DataFrame, lfc_threshold: float = 1.0, alpha: float = 0.05):
    """Draw a volcano plot and return the matplotlib Axes.

    matplotlib is imported lazily so importing this module (and running the unit
    tests) doesn't require a plotting backend to be installed.
    """
    import matplotlib.pyplot as plt

    data = volcano_data(results, lfc_threshold=lfc_threshold, alpha=alpha)
    colors = {"up": "#d62728", "down": "#1f77b4", "ns": "#999999"}

    fig, ax = plt.subplots(figsize=(6, 5))
    for category, group in data.groupby("category"):
        ax.scatter(
            group["log2_fold_change"],
            group["neg_log10_p"],
            s=10,
            c=colors[category],
            label=category,
            alpha=0.7,
        )
    ax.axvline(lfc_threshold, ls="--", c="grey", lw=0.8)
    ax.axvline(-lfc_threshold, ls="--", c="grey", lw=0.8)
    ax.set_xlabel("log2 fold change")
    ax.set_ylabel("-log10 p-value")
    ax.set_title("Volcano plot")
    ax.legend(title="regulation")
    return ax
