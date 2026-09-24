# Datasets

This directory does **not** contain dataset files or their pixel data. It has three layers:

1. **Fetch** — each subdirectory's `README.md` + `fetch.sh` (where licensing allows it) downloads
   raw files into a local, gitignored `data/<name>/` folder at the repo root.
2. **Index** — `biotransport_datasets/` builds a small Parquet file per dataset
   (`data/<name>/index.parquet`) holding file paths, labels, splits, and demographics — not image
   bytes. Even a 12k-row dataset indexes down to a few MB.
3. **Load** — `biotransport_datasets.loader` reads that small index eagerly (fits in memory, loads
   in under a second) and streams the actual image files off disk lazily, one at a time, as a
   training loop asks for them. Nothing decodes 10,000 images into RAM at once.

`datasets.yaml` is the registry both the fetch scripts and the Python layer read: what each
dataset is, where it comes from, its license, and whether an indexing recipe exists for it yet.

## Why not just commit the data?

Two hard blockers, not preferences:

- **Size.** Several of these (AI-READI is ~3.8TB; EyePACS is tens of GB) are far past GitHub's
  100MB per-file hard limit and would bloat the repo's history permanently even if they somehow
  fit. Git is not built for large binary datasets.
- **License/redistribution terms.** EyePACS, AI-READI, APTOS, and IDRiD are each gated behind an
  explicit usage attestation on their own platform (a Kaggle account accepting competition rules,
  IEEE DataPort registration, AI-READI's "state your research purpose" step). Copying the raw
  files into a different repo would likely violate those terms — for AI-READI specifically, that
  could jeopardize the team's ability to use the dataset at all if it surfaced.

## Quickstart (SMDG-19, the one actually in use for the glaucoma model)

```bash
cd datasets
pip install -r requirements.txt          # add pillow/torch too if you're training, not just indexing
./scripts/fetch_kaggle.sh dataset deathtrooper/multichannel-glaucoma-benchmark-dataset smdg-19-glaucoma
python -m biotransport_datasets.build smdg-19-glaucoma
```

Then, from Python (anywhere with `datasets/` on the path):

```python
from biotransport_datasets import load_split, BioTransportImageDataset

# Tabular-only — a plain dataframe, e.g. for the paper's 1D-CNN biomarker baseline
train_df = load_split("smdg-19-glaucoma", split="train", exclude_segmentation_leakage=True)

# Streaming images for the vision-transformer branches — nothing decoded until iterated
from torch.utils.data import DataLoader
ds = BioTransportImageDataset("smdg-19-glaucoma", exclude_segmentation_leakage=True,
                               numeric_columns=["age"])
dl = DataLoader(ds, batch_size=32, shuffle=True, num_workers=4)
```

## Why Parquet specifically

Compact (columnar + compression — a 12k-row index is single-digit MB), fast to filter/query
(`load_split(..., where="label == 1 and age >= 40")` doesn't touch a single image file), and reads
natively from pandas, polars, DuckDB, or Spark if the team's tooling ever changes. Raw images stay
as plain JPEG/PNG files on disk — Parquet is for the *index*, not for storing pixel data.

## Adding indexing support for another dataset

Only SMDG-19 has a recipe implemented so far (it's the one actually needed right now, for the
glaucoma model). To add another: copy `biotransport_datasets/recipes/_template.py`, implement
`build()` against that dataset's real downloaded layout (not guessed from docs — see the SMDG-19
recipe's comments for why that matters), and set `recipe: <name>` in `datasets.yaml`.

## Using this with an agent (e.g., for model development)

Follow the [`biotransport-data-workflow`](../.claude/skills/biotransport-data-workflow/SKILL.md)
skill: read the original files and the index, never modify them, write any derived output
(computed features, model predictions) via `write_derived()` to `data/<name>/derived/`, never back
into the indexed dataset itself.

## Setup once, before running any fetch script

- **Kaggle-hosted datasets** (SMDG-19, EyePACS, APTOS, EYES-DEFY-ANEMIA): install the `kaggle`
  CLI (`pip install kaggle`) and put your Kaggle API token at `~/.kaggle/kaggle.json` — generate
  one at kaggle.com/settings under "API." You also need to accept each dataset's/competition's
  terms on its Kaggle page at least once, in a browser, before the CLI can download it.
- **AI-READI**: no script — it's a manual portal flow (login, state research purpose, attest to
  usage terms) by design. See that folder's README.
- **Messidor-2, IDRiD, CP-AnemiC**: no script — I couldn't confirm a stable, unauthenticated
  download URL for any of these without a browser session, and I'm not going to ship a fetch
  script against a guessed one. Each folder's README says exactly what's needed manually.

## Contents

| Dataset | Condition | Access | Fetch script? | Index recipe? |
| --- | --- | --- | --- | --- |
| `smdg-19-glaucoma` | Glaucoma (imaging + demographics) | Kaggle | Yes | Yes |
| `eyepacs-diabetes` | Diabetes (imaging) | Kaggle | Yes | Not yet |
| `aptos2019-diabetes` | Diabetes (imaging) | Kaggle | Yes | Not yet |
| `messidor2-diabetes` | Diabetes (imaging) | Academic registration | No — manual | Not yet |
| `idrid-diabetes` | Diabetes (imaging) | IEEE DataPort | No — manual | Not yet |
| `ai-readi-diabetes` | Diabetes (multimodal) | FAIRhub portal | No — manual | Not yet |
| `cp-anemic` | Anemia (imaging) | Mendeley Data | No — manual (CC BY 4.0, confirmed) | Not yet |
| `eyes-defy-anemia` | Anemia (imaging) | Kaggle | Yes | Not yet |
| `idc-cancer-imaging` | Cancer (imaging) | Agentic API, not a bulk download | N/A | N/A |
