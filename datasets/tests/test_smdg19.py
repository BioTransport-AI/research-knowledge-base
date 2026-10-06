"""Tests for the SMDG-19 recipe against a synthetic fixture -- not the real 3GB
download. Covers the recipe's own logic (column mapping, mask-path resolution,
the stratified split) in isolation so it runs fast and without the dataset
fetched. scripts/validate_features_on_real_masks.py (glaucoma-model) is the
other half: it checks extract_features() against the *real* ground-truth
masks, which a synthetic fixture can't meaningfully stand in for.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from biotransport_datasets.recipes import smdg19


def _make_raw_dir(tmp_path: Path, *, n_per_label: int = 20) -> Path:
    """Build a tiny fake SMDG-19 raw_dir: real directory structure, no real
    image bytes needed since the recipe only ever looks at file *paths*."""
    raw_dir = tmp_path / "smdg-19-glaucoma"
    fundus_dir = raw_dir / smdg19.IMAGE_SUBDIR
    fundus_dir.mkdir(parents=True)

    rows = []
    image_id = 0
    for label in (0, 1, -1):
        for _ in range(n_per_label):
            name = f"img{image_id}"
            (fundus_dir / f"{name}.png").touch()
            rows.append({"fundus": f"{name}.png", "types": label, "age": 50, "sex": "M"})
            image_id += 1
    pd.DataFrame(rows).to_csv(raw_dir / smdg19.METADATA_FILENAME, index=False)

    # Give every 2nd image an optic-cup mask and every 3rd an optic-disc mask,
    # so overlap and non-overlap both exist -- a recipe bug that only shows up
    # when the two mask sets aren't identical would otherwise hide.
    cup_dir = raw_dir / smdg19.MASK_SUBDIRS["optic_cup_mask_path"]
    disc_dir = raw_dir / smdg19.MASK_SUBDIRS["optic_disc_mask_path"]
    cup_dir.mkdir(parents=True)
    disc_dir.mkdir(parents=True)
    for i in range(image_id):
        if i % 2 == 0:
            (cup_dir / f"img{i}.png").touch()
        if i % 3 == 0:
            (disc_dir / f"img{i}.png").touch()

    return raw_dir


def test_build_resolves_paths_and_label(tmp_path: Path) -> None:
    raw_dir = _make_raw_dir(tmp_path, n_per_label=5)
    df = smdg19.build(raw_dir)

    assert len(df) == 15
    assert set(df["label"]) == {0, 1, -1}
    assert all(Path(p).name.startswith("img") for p in df["file_path"])
    assert all(df["condition"] == "glaucoma")


def test_build_mask_paths_only_set_when_mask_exists(tmp_path: Path) -> None:
    raw_dir = _make_raw_dir(tmp_path, n_per_label=10)
    df = smdg19.build(raw_dir)

    has_cup = df["optic_cup_mask_path"].notna()
    for _, row in df.iterrows():
        image_num = int(row["image_id"].removeprefix("img"))
        assert has_cup[row.name] == (image_num % 2 == 0)
        if has_cup[row.name]:
            assert Path(row["optic_cup_mask_path"]).name == f"{row['image_id']}.png"

    # No macula recipe support -- see the MASK_SUBDIRS comment in smdg19.py.
    assert "macula_mask_path" not in df.columns


def test_build_used_for_segmentation_matches_any_mask_dir(tmp_path: Path) -> None:
    raw_dir = _make_raw_dir(tmp_path, n_per_label=10)
    df = smdg19.build(raw_dir)

    expected = df["optic_cup_mask_path"].notna() | df["optic_disc_mask_path"].notna()
    assert (df["used_for_segmentation"] == expected).all()


def test_build_split_is_stratified_and_covers_every_row(tmp_path: Path) -> None:
    raw_dir = _make_raw_dir(tmp_path, n_per_label=50)
    df = smdg19.build(raw_dir)

    assert set(df["split"]) == {"train", "val", "test"}
    assert df["split"].isna().sum() == 0

    for label in (0, 1, -1):
        counts = df.loc[df["label"] == label, "split"].value_counts()
        # 50 rows/label at 80:10:10 -> exactly 40/5/5, no rounding ambiguity.
        assert counts["train"] == 40
        assert counts["val"] == 5
        assert counts["test"] == 5


def test_build_split_is_reproducible_across_runs(tmp_path: Path) -> None:
    raw_dir = _make_raw_dir(tmp_path, n_per_label=20)
    first = smdg19.build(raw_dir).set_index("image_id")["split"]
    second = smdg19.build(raw_dir).set_index("image_id")["split"]
    assert first.equals(second)


def test_build_missing_metadata_file_raises(tmp_path: Path) -> None:
    raw_dir = tmp_path / "empty"
    raw_dir.mkdir()
    with pytest.raises(FileNotFoundError):
        smdg19.build(raw_dir)
