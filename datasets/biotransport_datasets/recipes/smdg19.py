"""Indexing recipe for SMDG-19 (Standardized Multi-Channel Dataset for Glaucoma).

IMPORTANT: the exact column names in metadata.csv are inferred from the dataset's
public documentation (its Kaggle page and the standardized-multichannel-dataset-
glaucoma GitHub README), not confirmed against the real file -- nobody on the team
had it downloaded yet when this was written. COLUMN_MAP below is the one place to
fix things if the real names differ; build_index() will fail with a clear message
(listing the actual columns it found) rather than silently building a wrong index
if the mapping doesn't match. Run once after fetching, fix COLUMN_MAP if needed,
rerun.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

# Left side: what we assume the CSV calls a column. Right side: what our index
# calls it. To check the real names:
#   python -c "import pandas as pd; print(pd.read_csv('data/smdg-19-glaucoma/metadata.csv').columns.tolist())"
COLUMN_MAP = {
    "fundus": "file_path",
    "names": "file_path",
    "types": "label",
    "class": "label",
    "age": "age",
    "sex": "sex",
    "gender": "sex",
}

IMAGE_SUBDIR = "full-fundus"
SEGMENTATION_SUBDIRS = ["optic-cup", "optic-disc", "blood-vessel", "vessel-artery", "vessel-vein"]


def build(raw_dir: Path) -> pd.DataFrame:
    metadata_path = raw_dir / "metadata.csv"
    if not metadata_path.exists():
        raise FileNotFoundError(
            f"{metadata_path} not found -- did the Kaggle download finish? "
            f"Expected metadata.csv at the root of {raw_dir}."
        )

    raw = pd.read_csv(metadata_path)
    rename = {src: dst for src, dst in COLUMN_MAP.items() if src in raw.columns}
    if "file_path" not in rename.values() or "label" not in rename.values():
        raise ValueError(
            "Couldn't find the expected image-path or label column in metadata.csv.\n"
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
