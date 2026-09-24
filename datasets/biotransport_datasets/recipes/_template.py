"""Template for a new dataset's indexing recipe.

To add indexing support for a dataset that's currently `recipe: null` in
datasets.yaml:

1. Copy this file to recipes/<name>.py (use the dataset's `name` from
   datasets.yaml, with hyphens turned into underscores -- e.g. "eyepacs-diabetes"
   becomes eyepacs_diabetes.py).
2. Set `recipe: eyepacs_diabetes` (no .py, no quotes needed) for that entry in
   datasets.yaml.
3. Implement build() below against the dataset's actual downloaded layout --
   don't guess at column names/folder structure from documentation the way
   smdg19.py had to; write this one by actually looking at the files once
   they're fetched.
4. Run `python -m biotransport_datasets.build <name>` (see indexing.py /
   the datasets/README.md) to build the index and sanity-check the output.

build() must return a pandas DataFrame with at least these columns:
  - file_path: absolute or repo-relative path to the image file
  - condition: the disease/condition this row is for (matches datasets.yaml)
  - label: whatever this dataset's classification target is (name it clearly
    in this dataset's README if it's not a simple 0/1)

Add whatever else is useful (image_id, split, age, sex, ...) -- indexing.py only
enforces the three required columns, everything else is free-form per dataset.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def build(raw_dir: Path) -> pd.DataFrame:
    raise NotImplementedError(
        "Copy this template to recipes/<name>.py and implement build() against "
        "the dataset's actual downloaded layout."
    )
