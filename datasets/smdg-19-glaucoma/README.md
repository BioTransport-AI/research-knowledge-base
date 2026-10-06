# SMDG-19 (Standardized Multi-Channel Dataset for Glaucoma)

**Condition:** Glaucoma · **Modality:** Fundus images, segmentation masks, and demographics
**Source:** [Kaggle](https://www.kaggle.com/datasets/deathtrooper/multichannel-glaucoma-benchmark-dataset)
(compiled from the [GitHub project](https://github.com/TheBeastCoding/standardized-multichannel-dataset-glaucoma))
**Size:** 12,449 labeled instances (12.5k full-fundus images, 512x512 standardized)

## Why this one

This is the exact dataset used in Dr. Penkova's own paper: [Parikh, Nguyen & Penkova,
"Multimodal glaucoma classification using segmentation based biomarker extraction,"
Knowledge-Based Systems 349 (2026)](https://doi.org/10.1016/j.knosys.2026.116449). See the
tracker's Glaucoma Model tab for the full architecture and results built on it. Reproducing their
pipeline starts here.

## What's in it

Standardizes 19 public glaucoma datasets (REFUGE, ORIGA, AIROGS, DRISHTI-GS1, and others; full
list and per-source counts in `metadata - standardized.csv` once downloaded) into one consistent
format.

- **Labels:** 7,549 non-glaucoma, 4,767 glaucoma, 133 glaucoma-suspect (verified against the real
  download; counts in the original Kaggle documentation are approximate and drift slightly from
  this)
- **Segmentation masks:** optic cup (2,874 instances), optic disc (3,103), blood vessels (462,
  separated into artery/vein subsets), plus OCT images and OCT segmentation lines for a subset
- **Demographics:** age and sex where available, in `metadata - standardized.csv`
- **Folders:** `full-fundus/`, `optic-cup/`, `optic-disc/`, `blood-vessel/`, `vessel-artery/`,
  `vessel-vein/`, `spectral-oct/`, `spectral-oct-cup/`, `spectral-oct-disc/` (each one has its own
  redundant nested folder of the same name before the actual image files)

**Leakage note (from the paper):** for classification (not segmentation) work, two filters apply,
not one. First drop the 133 glaucoma-suspect rows (the paper's pipeline is strictly 2-class), then
exclude the images used to train the segmentation models. Doing both in that order lands on
exactly 8,818 samples, matching the paper's reported classification set precisely.
`glaucoma_model.data.load_classification_split()` in the glaucoma-model repo does this for you.
Skipping the suspect-label filter and only excluding segmentation leakage gives 8,883, which looks
close enough to be mistaken for the real number but is not it.

## Fetch

```bash
../scripts/fetch_kaggle.sh dataset deathtrooper/multichannel-glaucoma-benchmark-dataset smdg-19-glaucoma
```

Lands in `data/smdg-19-glaucoma/`. Requires the Kaggle CLI and API token, see the parent
`datasets/README.md`.

## Then build the index

```bash
python -m biotransport_datasets.build smdg-19-glaucoma
```

This is the only dataset here with an indexing recipe implemented so far
(`biotransport_datasets/recipes/smdg19.py`), verified against the real downloaded data, including
real mask file paths and a stratified train/val/test split. See the parent README's Quickstart for
how to load splits or stream images from the result.
