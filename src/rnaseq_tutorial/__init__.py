"""rnaseq_tutorial — a toy RNA-seq differential expression package.

The whole point of putting logic in an installable package (instead of notebooks)
is that it can be *imported*, *tested*, and *reused*. Notebooks call into this code;
they don't define the important logic themselves.
"""

from rnaseq_tutorial.data import load_counts, simulate_counts
from rnaseq_tutorial.features import filter_low_counts, normalize_cpm
from rnaseq_tutorial.model import differential_expression

__version__ = "0.1.0"

__all__ = [
    "load_counts",
    "simulate_counts",
    "filter_low_counts",
    "normalize_cpm",
    "differential_expression",
]
