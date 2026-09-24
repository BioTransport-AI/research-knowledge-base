"""Build and read the Parquet index for a dataset.

The index is the whole point of this layer: it holds file paths, labels, splits,
and (once computed) derived biomarker features as *rows of a small table* -- a few
MB even for tens of thousands of images -- so it comfortably fits in memory and
loads in under a second. The actual image bytes never go through this module;
`loader.py` reads them lazily, one file at a time, off the paths this index stores.

Read-only-source rule applies here same as everywhere else (see the
biotransport-data-workflow skill): building an index only *reads* the raw dataset
directory (images, the original metadata.csv) and *writes* to index.parquet --
never touches the raw files themselves.
"""

from __future__ import annotations

import importlib
from pathlib import Path

import pandas as pd

from . import config

REQUIRED_COLUMNS = {"file_path", "condition", "label"}


def build_index(name: str, *, force: bool = False) -> pd.DataFrame:
    """Build (or load a cached) Parquet index for a registered dataset.

    Delegates the actual "how do I read this dataset's specific layout" logic to
    that dataset's recipe module (biotransport_datasets/recipes/<recipe>.py),
    which must expose a `build(raw_dir: Path) -> pd.DataFrame` function. This
    function handles the shared bookkeeping: locating the raw dir, validating the
    recipe's output has the columns everything downstream expects, caching to
    Parquet, and not re-running the recipe unnecessarily.
    """
    spec = config.get_spec(name)
    if spec.recipe is None:
        raise NotImplementedError(
            f"{name} has no indexing recipe yet (see datasets.yaml). "
            f"Add biotransport_datasets/recipes/{name.replace('-', '_')}.py -- "
            f"copy recipes/_template.py as a starting point."
        )

    if spec.index_path.exists() and not force:
        return read_index(name)

    if not spec.raw_dir.exists():
        raise FileNotFoundError(
            f"{spec.raw_dir} doesn't exist yet. Run the fetch script/manual steps "
            f"in datasets/{name}/README.md first."
        )

    recipe = importlib.import_module(f".recipes.{spec.recipe}", package=__package__)
    df = recipe.build(spec.raw_dir)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            f"recipes.{spec.recipe}.build() is missing required columns {missing}. "
            f"Every recipe must produce at least {REQUIRED_COLUMNS}."
        )
    if "dataset" not in df.columns:
        df = df.assign(dataset=name)

    spec.index_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(spec.index_path, engine="pyarrow", compression="zstd", index=False)
    return df


def read_index(name: str) -> pd.DataFrame:
    spec = config.get_spec(name)
    if not spec.index_path.exists():
        raise FileNotFoundError(
            f"No index at {spec.index_path} yet -- call build_index({name!r}) first."
        )
    return pd.read_parquet(spec.index_path, engine="pyarrow")


def write_derived(name: str, derived_name: str, df: pd.DataFrame, key: str = "image_id") -> Path:
    """Write a derived table (computed features, a model's predictions, anything
    downstream of the raw index) to data/<name>/derived/<derived_name>.parquet.

    Never call this with a path inside the dataset's raw_dir -- derived output
    always lives in its own `derived/` subfolder, keeping the read-only-source
    line unambiguous. `key` should be a column that lets callers join back to the
    base index later (e.g. the same image_id/file_path the index uses).
    """
    spec = config.get_spec(name)
    if key not in df.columns:
        raise ValueError(f"derived table must include the join key {key!r} to be usable later")
    out_dir = spec.raw_dir.parent / "derived" if spec.local_dir else None
    if out_dir is None:
        raise ValueError(f"{name} has no local_dir to derive alongside")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{derived_name}.parquet"
    df.to_parquet(out_path, engine="pyarrow", compression="zstd", index=False)
    return out_path
