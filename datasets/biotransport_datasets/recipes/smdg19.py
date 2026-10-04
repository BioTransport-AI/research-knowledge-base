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

    keep = ["image_id", "file_path", "condition", "label", "used_for_segmentation"]
    for optional in ("age", "sex"):
        if optional in df.columns:
            keep.append(optional)
    return df[keep]
