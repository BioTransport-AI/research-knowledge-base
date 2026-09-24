# Datasets

This directory does **not** contain dataset files. Each subdirectory has a `README.md`
(source, size, license/terms, what's in it) and, where the license allows scripted access,
a `fetch.sh` that downloads it into a local, gitignored `data/` folder at the repo root.

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

Scripted, on-demand fetching gets the same practical outcome — clone the repo, run one command,
data is ready for an agent or a training script to read — without either problem.

## Using this with an agent (e.g., for model development)

Read datasets from wherever `fetch.sh` puts them (`data/<dataset-name>/`), never from inside this
`datasets/` directory itself (that's docs and scripts only). Follow the
[`biotransport-data-workflow`](../.claude/skills/biotransport-data-workflow/SKILL.md) skill:
read the original files, never modify them, write any derived output (features, splits, trained
model artifacts) to a separate location.

## Setup once, before running any fetch script

Most of these need credentials the scripts can't obtain for you:

- **Kaggle-hosted datasets** (SMDG-19, EyePACS, APTOS, EYES-DEFY-ANEMIA): install the `kaggle`
  CLI (`pip install kaggle`) and put your Kaggle API token at `~/.kaggle/kaggle.json` — generate
  one at kaggle.com/settings under "API." You also need to accept each dataset's/competition's
  terms on its Kaggle page at least once, in a browser, before the CLI can download it.
- **AI-READI**: no script — it's a manual portal flow (login, state research purpose, attest to
  usage terms) by design. See that folder's README.
- **Messidor-2, IDRiD, CP-AnemiC**: no script — I couldn't confirm a stable, unauthenticated
  download URL for any of these without a browser session, and I'm not going to ship a fetch
  script against a guessed one. Each folder's README says exactly what's needed manually; these
  are easy to script later once someone confirms the real URL.

## Contents

| Dataset | Condition | Access | Script? |
| --- | --- | --- | --- |
| `smdg-19-glaucoma` | Glaucoma (imaging + demographics) | Kaggle | Yes |
| `eyepacs-diabetes` | Diabetes (imaging) | Kaggle | Yes |
| `aptos2019-diabetes` | Diabetes (imaging) | Kaggle | Yes |
| `messidor2-diabetes` | Diabetes (imaging) | Academic registration | No — manual |
| `idrid-diabetes` | Diabetes (imaging) | IEEE DataPort | No — manual |
| `ai-readi-diabetes` | Diabetes (multimodal) | FAIRhub portal | No — manual |
| `cp-anemic` | Anemia (imaging) | Mendeley Data | No — manual (CC BY 4.0, confirmed) |
| `eyes-defy-anemia` | Anemia (imaging) | Kaggle | Yes |
| `idc-cancer-imaging` | Cancer (imaging) | Agentic API, not a bulk download | N/A — see its README |
