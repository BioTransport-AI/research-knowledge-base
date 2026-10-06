"""Indexing recipe for SMDG-19 (Standardized Multi-Channel Dataset for Glaucoma).

Verified against the real download (2026-10-03, 12,449 rows, 48 columns).
The metadata file is named "metadata - standardized.csv", not "metadata.csv"
-- the Kaggle page's docs don't mention the space/suffix. Two of the original
column guesses actively collided with a second real column mapping to the
same target (pandas silently creates duplicate-named columns on rename
rather than erroring, which then breaks downstream with a confusing error
far from the real cause):
  - "names" was guessed as an alternate for file_path, but it holds bare IDs
    with no file extension ("OIA-ODIR-TEST-OFFLINE-1"), not a usable path.
    "fundus" (e.g. "/full-fundus/OIA-ODIR-TEST-OFFLINE-1.png") is the real one.
  - "gender" was guessed as an alternate for sex, but it's 90% empty
    (488 of 12,449 rows) -- "sex" is the populated column (4,516 non-null;
    the rest are presumably from sub-datasets that didn't record it at all).

"types" is the real label column: 0 = non-glaucoma (7,549), 1 = glaucoma
(4,767), -1 = glaucoma-suspect (133) -- matches the documented ~7,499 /
~4,817 / 133 split closely enough to be clearly the right column (small
drift is consistent with a dataset version update since the docs were
written). "type_expanded" has finer-grained, human-readable subtypes but is
NaN for nearly half the rows, so it's not usable as the primary label.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

COLUMN_MAP = {
    "fundus": "file_path",
    "types": "label",
    "age": "age",
    "sex": "sex",
}

METADATA_FILENAME = "metadata - standardized.csv"

# Each top-level folder from the Kaggle zip contains one redundant nested
# folder of the same name before the actual images -- e.g. the real files are
# at full-fundus/full-fundus/*.png, not full-fundus/*.png. Verified against
# the real download: counts match the paper's documented figures exactly
# (full-fundus 12,449; optic-disc 3,103; optic-cup 2,874; blood-vessel 462).
IMAGE_SUBDIR = "full-fundus/full-fundus"
SEGMENTATION_SUBDIRS = [
    "optic-cup/optic-cup",
    "optic-disc/optic-disc",
    "blood-vessel/blood-vessel",
    "vessel-artery/vessel-artery",
    "vessel-vein/vessel-vein",
]

# The subset of SEGMENTATION_SUBDIRS that glaucoma_model.features.extract_features()
# actually consumes (vasculature_density() takes the blood-vessel mask specifically,
# not artery/vein separately -- see that module's docstring). Captured as real paths,
# not just the leakage boolean below, because the segmentation stage needs to load
# these images as training targets, not merely know a mask exists.
MASK_SUBDIRS = {
    "optic_cup_mask_path": "optic-cup/optic-cup",
    "optic_disc_mask_path": "optic-disc/optic-disc",
    "vasculature_mask_path": "blood-vessel/blood-vessel",
}

# No macula masks exist anywhere in the public SMDG-19 download (verified: zero
# files under any "*macula*" path). The paper's macula ground truth (Section 3.5)
# is a separate, manual annotation the authors did themselves on 728 images via
# Roboflow -- it was never part of SMDG-19's public release. There is nothing to
# add a MASK_SUBDIRS entry for; reproducing the macula/SegFormer stage will
# require the team to annotate its own macula masks, same as the paper's authors
# did, not a recipe fix. Tracked in glaucoma-model's README under Known gaps.

# Stratify-by-label train/val/test split, assigned once across the whole index at
# build time so every downstream task (classification, each segmentation structure)
# filters the *same* assignment rather than each caller re-splitting independently
# -- the only way to guarantee a classification-train image and a segmentation-train
# image were never meant to land on opposite sides of a boundary. Ratios and the
# stratify-by-label choice match the paper's own "stratified splits... in 80:10:10
# ratio" (Section 3.1); the paper doesn't restate the stratify key for the
# per-structure segmentation splits in 3.2-3.5, so this applies the one convention
# it does state everywhere else it's explicit.
SPLIT_RATIOS = (0.8, 0.1, 0.1)
SPLIT_SEED = 42


def _assign_stratified_split(labels: pd.Series) -> pd.Series:
    rng = np.random.RandomState(SPLIT_SEED)
    split = pd.Series(index=labels.index, dtype=object)
    for _, group in labels.groupby(labels):
        idx = group.index.to_numpy().copy()
        rng.shuffle(idx)
        n = len(idx)
        n_train = int(round(n * SPLIT_RATIOS[0]))
        n_val = int(round(n * SPLIT_RATIOS[1]))
        split.loc[idx[:n_train]] = "train"
        split.loc[idx[n_train : n_train + n_val]] = "val"
        split.loc[idx[n_train + n_val :]] = "test"
    return split


def build(raw_dir: Path) -> pd.DataFrame:
    metadata_path = raw_dir / METADATA_FILENAME
    if not metadata_path.exists():
        raise FileNotFoundError(
            f"{metadata_path} not found -- did the Kaggle download finish? "
            f"Expected '{METADATA_FILENAME}' at the root of {raw_dir}."
        )

    raw = pd.read_csv(metadata_path)
    rename = {src: dst for src, dst in COLUMN_MAP.items() if src in raw.columns}
    if "file_path" not in rename.values() or "label" not in rename.values():
        raise ValueError(
            f"Couldn't find the expected image-path or label column in {METADATA_FILENAME}.\n"
            f"Actual columns: {raw.columns.tolist()}\n"
            f"COLUMN_MAP only matched: {rename}\n"
            "Update COLUMN_MAP at the top of this file to match, then rerun."
        )
    df = raw.rename(columns=rename)

    # Resolve to absolute paths under full-fundus/ so the loader can open them
    # directly regardless of whether the CSV stored a bare filename or a relative path.
    fundus_dir = raw_dir / IMAGE_SUBDIR
    df["file_path"] = df["file_path"].apply(lambda name: str(fundus_dir / Path(name).name))
    df["image_id"] = df["file_path"].apply(lambda p: Path(p).stem)
    df["condition"] = "glaucoma"

    # Flag rows whose image also has a mask in a segmentation folder -- assumes
    # mask filenames share the fundus image's stem (the common convention for
    # paired image/mask datasets; verify if the leakage flag looks wrong).
    # These were used to train the paper's segmentation models and should be
    # excluded from classification splits to avoid leakage -- see the paper's
    # methodology and the Glaucoma Model tab in the tracker.
    seg_ids: set[str] = set()
    for sub in SEGMENTATION_SUBDIRS:
        seg_dir = raw_dir / sub
        if seg_dir.exists():
            seg_ids.update(p.stem for p in seg_dir.glob("*"))
    df["used_for_segmentation"] = df["image_id"].isin(seg_ids)

    # Real mask paths for the structures extract_features() consumes -- NaN where
    # this image has no mask for that structure (most rows: only 2,874 of 12,449
    # have an optic-cup mask, for instance). Same stem-matching assumption as the
    # leakage flag above.
    mask_cols = []
    for col_name, sub in MASK_SUBDIRS.items():
        mask_dir = raw_dir / sub
        paths_by_id = {p.stem: str(p) for p in mask_dir.glob("*")} if mask_dir.exists() else {}
        df[col_name] = df["image_id"].map(paths_by_id)
        mask_cols.append(col_name)

    # One global split, stratified by label, assigned once here so every caller
    # (classification, each segmentation structure) filters the same assignment --
    # see _assign_stratified_split()'s docstring comment above for why that matters.
    df["split"] = _assign_stratified_split(df["label"])

    keep = ["image_id", "file_path", "condition", "label", "used_for_segmentation", "split", *mask_cols]
    for optional in ("age", "sex"):
        if optional in df.columns:
            keep.append(optional)
    return df[keep]
