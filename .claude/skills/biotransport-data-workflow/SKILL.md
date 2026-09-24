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

## Practical pattern

1. Load the original dataset from wherever it's stored (local download, mounted drive, or queried
   live via an interface like IDC's agentic API) — read-only.
2. Do the actual work (feature engineering, model input prep, analysis) into memory or a working
   dataframe.
3. Write the result to a new, clearly-named location. Never overwrite step 1's source.
4. If the derived output is something the team will reuse, note what it is and how it was built
   (briefly — not a full methods section) wherever the team tracks that kind of thing, so nobody
   has to reverse-engineer it later.

## Distribution note

The Free Data reference itself should live in more than one place for people who don't work out of
the repo day to day: the GitHub repo (`tracker-snapshots/`, already done) and Google Drive (a
manual step — no Drive connector is set up for Claude to do this automatically as of 2026-09-24).
