"""Generate the bundled toy dataset into data/raw/.

In a real project this script would download from GEO/SRA/an S3 bucket/a LIMS.
Here it simulates data so the repo is self-contained. Either way, the pattern
is the same: a *script* produces data/raw/, and nothing downstream edits it.

    python scripts/download_data.py
"""

from pathlib import Path

from rnaseq_tutorial.data import simulate_counts

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    counts, labels = simulate_counts(seed=0)
    counts.to_csv(RAW_DIR / "counts.csv")
    labels.to_csv(RAW_DIR / "sample_metadata.csv", header=True)
    print(f"Wrote {counts.shape[0]} genes x {counts.shape[1]} samples to {RAW_DIR}/")


if __name__ == "__main__":
    main()
