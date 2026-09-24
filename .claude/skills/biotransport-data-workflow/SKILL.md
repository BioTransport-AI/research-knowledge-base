---
name: biotransport-data-workflow
description: How to read and work with BioTransport AI's research datasets (the ones listed in the tracker's Free Data tab and Data sources table) safely — read the originals, never modify them, write any derived work to new files. Use this whenever Noah, Dr. Penkova, or Andy asks to explore, analyze, feature-engineer, or build on a dataset, or asks an agent to "work with the data" — even if they don't name this skill directly.
---

# Working with BioTransport AI's datasets

The team's datasets (AI-READI, EyePACS, CP-AnemiC, IDC collections, and the rest — see the
tracker's "Free Data: Ready Now" tab) are shared, external, and often hard to re-download or
re-request. Treat every original file as read-only, always. This isn't a formality — it's the
difference between an experiment that can be rerun and one that silently corrupted its own input.

## The rule

- **Read the original dataset. Never write to it, rename it, or reorganize its files.**
- **Any transformation — feature engineering, filtering, relabeling, augmentation, merged tables —
  goes into a new file or table**, clearly named and placed outside the original dataset's
  directory (e.g. `derived/<dataset-name>/<what-it-is>.parquet`, not inside the dataset's own
  folder).
- **Name derived outputs for what they contain and how they were made**, not just "processed" or
  "v2" — a future session (or teammate) should be able to tell what a derived table is without
  re-running the code that made it.
- If a task seems to call for editing a dataset in place (fixing a bad label, deduplicating rows),
  don't — write the correction as a derived table or a patch file instead, and say so explicitly
  rather than quietly overwriting.

## Why this matters here specifically

Most of these datasets came from outreach, gated access, or a one-time download — AI-READI's
controlled tier, ORIGA and OHTS pending replies, IDC's agentic interface. Re-acquiring one because
a local copy got corrupted isn't a quick retry, it can mean re-running a whole access request. The
read-only convention exists so experimentation is always safe to redo from scratch.

## Practical pattern — use the actual tooling, don't hand-roll this each time

`datasets/biotransport_datasets/` (added 2026-09-24) implements this pattern concretely — use it
rather than writing ad hoc pandas/PIL loading code per task:

1. Fetch raw files via that dataset's `fetch.sh` (or manual steps) into gitignored `data/<name>/`
   — read-only from here on.
2. Build a small Parquet **index** over it (`python -m biotransport_datasets.build <name>`, or
   `build_index()` in Python) — file paths, labels, splits, demographics, not pixel data. This is
   the only thing that gets loaded eagerly; it's a few MB even for tens of thousands of rows.
3. Read images lazily off that index during actual work — `load_split()` for a plain dataframe
   (tabular-only), or `BioTransportImageDataset` (a lazy `torch.utils.data.Dataset`) when you need
   the actual pixels, so nothing decodes more than one batch of images into memory at a time.
4. Write any derived output (computed features, predictions, splits) via `write_derived()` to
   `data/<name>/derived/<what-it-is>.parquet` — never back into the index or the raw files.

Only SMDG-19 has a recipe (step 2) implemented so far — see
`datasets/biotransport_datasets/recipes/_template.py` for adding another, and do it against the
dataset's real downloaded layout, not guessed column names from documentation.

## Distribution note

The Free Data reference itself should live in more than one place for people who don't work out of
the repo day to day: the GitHub repo (`tracker-snapshots/`, already done) and Google Drive (a
manual step — no Drive connector is set up for Claude to do this automatically as of 2026-09-24).
