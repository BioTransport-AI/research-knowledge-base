# SMDG-19 (Standardized Multi-Channel Dataset for Glaucoma)

**Condition:** Glaucoma · **Modality:** Fundus images + segmentation masks + demographics
**Source:** [Kaggle](https://www.kaggle.com/datasets/deathtrooper/multichannel-glaucoma-benchmark-dataset)
(compiled from the [GitHub project](https://github.com/TheBeastCoding/standardized-multichannel-dataset-glaucoma))
**Size:** ~12,449 labeled instances (12.5k full-fundus images, 512×512 standardized)

## Why this one

This is the exact dataset used in Dr. Penkova's own paper — [Parikh, Nguyen & Penkova,
"Multimodal glaucoma classification using segmentation based biomarker extraction,"
Knowledge-Based Systems 349 (2026)](https://doi.org/10.1016/j.knosys.2026.116449) — see the
tracker's Glaucoma Model tab for the full architecture and results built on it. Reproducing their
pipeline starts here.

## What's in it

Standardizes 19 public glaucoma datasets (REFUGE, ORIGA, AIROGS, DRISHTI-GS1, and others — full
list and per-source counts in `metadata.csv` once downloaded) into one consistent format.

- **Labels:** 7,499 non-glaucoma, 4,817 glaucoma, 133 glaucoma-suspect
- **Segmentation masks:** optic cup (2,874 instances), optic disc (3,103), blood vessels (462,
  separated into artery/vein subsets), plus OCT images and OCT segmentation lines for a subset
- **Demographics:** age and sex where available, in `metadata.csv`
- **Folders:** `full-fundus/`, `optic-cup/`, `optic-disc/`, `blood-vessel/`, `vessel-artery/`,
  `vessel-vein/`, `spectral-oct/`, `spectral-oct-cup/`, `spectral-oct-disc/`

**Leakage note (from the paper):** for classification (not segmentation) work, exclude the images
used to train the segmentation models first — the paper's classification set is 8,818 samples
after that exclusion, not the full 12,449. Don't skip this step if reproducing their numbers.

## Fetch

```bash
../scripts/fetch_kaggle.sh dataset deathtrooper/multichannel-glaucoma-benchmark-dataset smdg-19-glaucoma
```

Lands in `data/smdg-19-glaucoma/`. Requires the Kaggle CLI and API token — see the parent
`datasets/README.md`.
