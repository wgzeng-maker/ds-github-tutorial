"""Tests for the volcano-plot data preparation.

We test the *pure* function (volcano_data), not the drawing, because the logic
worth protecting is the categorization — not matplotlib's pixels.
"""

import pandas as pd

from rnaseq_tutorial.plots import volcano_data


def _results():
    # Three hand-crafted genes: clearly up, clearly down, and not significant.
    return pd.DataFrame(
        {
            "log2_fold_change": [3.0, -2.5, 0.1],
            "p_value": [1e-8, 1e-7, 0.6],
            "p_adj": [1e-6, 1e-5, 0.8],
        },
        index=["UP", "DOWN", "NS"],
    )


def test_volcano_data_categorizes_genes():
    out = volcano_data(_results(), lfc_threshold=1.0, alpha=0.05)
    assert out.loc["UP", "category"] == "up"
    assert out.loc["DOWN", "category"] == "down"
    assert out.loc["NS", "category"] == "ns"


def test_volcano_data_adds_neg_log10_p():
    out = volcano_data(_results())
    # -log10(1e-8) == 8
    assert abs(out.loc["UP", "neg_log10_p"] - 8.0) < 1e-9
