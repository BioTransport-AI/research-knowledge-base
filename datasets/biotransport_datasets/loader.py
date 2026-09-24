"""Streaming access to indexed datasets: read the (small) Parquet index eagerly,
read image bytes off disk lazily, one at a time, exactly when a training loop asks
for them. This is what keeps a 12k-image dataset from needing 12k decoded images
sitting in RAM at once -- only the current batch does.

torch is imported lazily inside the class that needs it, so `pip install
pandas pyarrow pyyaml pillow` alone is enough to build/inspect indexes; you only
need torch installed if you're actually going to train with this.
"""

from __future__ import annotations

from typing import Callable, Optional

import pandas as pd

from . import indexing

try:
    from torch.utils.data import Dataset as _TorchDataset
except ImportError:  # torch not installed -- indexing/tabular use still works fine
    _TorchDataset = object


def load_split(
    name: str,
    split: Optional[str] = None,
    where: Optional[str] = None,
    exclude_segmentation_leakage: bool = False,
) -> pd.DataFrame:
    """Read a dataset's index and return the rows you actually want to train/test
    on -- this is the "just give me a dataframe" entry point for anyone doing
    tabular-only work (no images), or who wants to build their own loader.

    `where` is a pandas query string, e.g. "label == 1 and age >= 40".
    `exclude_segmentation_leakage` drops rows flagged `used_for_segmentation` --
    relevant for SMDG-19 specifically, see the Parikh/Nguyen/Penkova paper.
    """
    df = indexing.read_index(name)
    if split is not None and "split" in df.columns:
        df = df[df["split"] == split]
    if exclude_segmentation_leakage and "used_for_segmentation" in df.columns:
        df = df[~df["used_for_segmentation"]]
    if where:
        df = df.query(where)
    return df.reset_index(drop=True)


class BioTransportImageDataset(_TorchDataset):
    """A torch.utils.data.Dataset over one dataset's indexed images.

    Usage:
        from biotransport_datasets.loader import BioTransportImageDataset
        from torch.utils.data import DataLoader

        ds = BioTransportImageDataset("smdg-19-glaucoma", split="train",
                                       exclude_segmentation_leakage=True)
        dl = DataLoader(ds, batch_size=32, shuffle=True, num_workers=4)
        for images, labels, numeric_features in dl:
            ...

    Each item is (PIL.Image or transformed tensor, label, numeric-feature dict) --
    nothing is decoded until __getitem__ is actually called, so a DataLoader with
    num_workers > 0 parallelizes the disk reads across processes instead of
    blocking training on them one at a time.
    """

    def __init__(
        self,
        name: str,
        split: Optional[str] = None,
        where: Optional[str] = None,
        exclude_segmentation_leakage: bool = False,
        transform: Optional[Callable] = None,
        numeric_columns: Optional[list[str]] = None,
    ):
        self.name = name
        self.df = load_split(
            name, split=split, where=where,
            exclude_segmentation_leakage=exclude_segmentation_leakage,
        )
        self.transform = transform
        self.numeric_columns = numeric_columns or []

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, idx: int):
        from PIL import Image  # local import: only needed once you actually load an image

        row = self.df.iloc[idx]
        image = Image.open(row["file_path"]).convert("RGB")
        if self.transform is not None:
            image = self.transform(image)
        label = row["label"]
        numeric = {col: row[col] for col in self.numeric_columns if col in row}
        return image, label, numeric
