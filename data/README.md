# Data directory

**Nothing in `raw/` or `processed/` is committed to git** (see the repo `.gitignore`).
Only this README and `.gitkeep` placeholder files are tracked, so the folder structure
exists on a fresh clone.

## Why not commit data?

- **Size** — git is built for text/code, not gigabyte BAM/FASTQ/h5ad files. It bloats
  the repo and every clone forever, even after you delete the file.
- **Reproducibility** — `processed/` is *output*. It should always be regenerable from
  `raw/` + code. Committing it invites silent drift between data and code.
- **Privacy** — patient/clinical data often legally cannot live in a shared repo.

## So where does data go?

| Scale / need                    | Tool                                             |
|---------------------------------|--------------------------------------------------|
| Small files you want versioned  | [git-LFS](https://git-lfs.com/)                  |
| Versioned data + pipelines      | [DVC](https://dvc.org/)                           |
| Large / shared datasets         | S3, GCS, an institutional bucket                 |
| Public bio data                 | GEO, SRA, ENA — referenced by accession in code  |

## The layout

```
data/
├── raw/         # Immutable source data. Treat as read-only. Never hand-edit.
└── processed/   # Derived from raw/ by code. Safe to delete & regenerate anytime.
```

To populate this folder in the tutorial:

```bash
python scripts/download_data.py   # writes raw/counts.csv + raw/sample_metadata.csv
python scripts/run_pipeline.py    # writes processed/de_results.csv
```
