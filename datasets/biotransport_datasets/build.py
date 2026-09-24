"""CLI: build (or rebuild) a dataset's Parquet index.

    python -m biotransport_datasets.build smdg-19-glaucoma
    python -m biotransport_datasets.build smdg-19-glaucoma --force
    python -m biotransport_datasets.build --all

Run from the datasets/ directory (or anywhere, as long as biotransport_datasets/
is on PYTHONPATH -- `cd datasets && python -m biotransport_datasets.build ...`
is the simplest way).
"""

from __future__ import annotations

import argparse
import sys

from . import config
from .indexing import build_index


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", nargs="?", help="dataset name from datasets.yaml")
    parser.add_argument("--all", action="store_true", help="build every dataset that has a recipe")
    parser.add_argument("--force", action="store_true", help="rebuild even if index.parquet exists")
    args = parser.parse_args()

    if not args.all and not args.name:
        parser.error("pass a dataset name, or --all")

    names = [s.name for s in config.with_recipe()] if args.all else [args.name]

    for name in names:
        print(f"Building index for {name}...")
        try:
            df = build_index(name, force=args.force)
        except (FileNotFoundError, NotImplementedError, ValueError) as e:
            print(f"  skipped: {e}", file=sys.stderr)
            continue
        print(f"  {len(df)} rows -> {config.get_spec(name).index_path}")


if __name__ == "__main__":
    main()
