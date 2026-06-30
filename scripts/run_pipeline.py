"""Run the full analysis end-to-end: raw counts -> differential expression results.

This is the "reproducible result" in action. Given data/raw/ and this code,
anyone can regenerate data/processed/de_results.csv exactly.

    python scripts/run_pipeline.py
"""

from pathlib import Path

import pandas as pd

from rnaseq_tutorial.data import load_counts
from rnaseq_tutorial.model import differential_expression

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"


def main() -> None:
    if not (RAW_DIR / "counts.csv").exists():
        raise SystemExit("No data found. Run `python scripts/download_data.py` first.")

    counts = load_counts(RAW_DIR / "counts.csv")
    labels = pd.read_csv(RAW_DIR / "sample_metadata.csv", index_col=0)["group"]

    results = differential_expression(counts, labels)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out = PROCESSED_DIR / "de_results.csv"
    results.to_csv(out)

    n_sig = int(results["significant"].sum())
    print(f"Tested {len(results)} genes; {n_sig} significant at FDR < 0.05.")
    print(f"Top hits:\n{results.head()}")
    print(f"\nWrote results to {out}")


if __name__ == "__main__":
    main()
