#!/usr/bin/env bash
# Shared helper: download and unzip a Kaggle dataset or competition into data/<name>/.
# Requires: pip install kaggle, and ~/.kaggle/kaggle.json with your API token.
# You must also accept the dataset's/competition's terms on its Kaggle page in a browser
# at least once before the CLI can download it.
#
# Usage:
#   fetch_kaggle.sh dataset <owner>/<dataset-slug> <dest-name>
#   fetch_kaggle.sh competition <competition-slug> <dest-name>

set -euo pipefail

KIND="${1:?usage: fetch_kaggle.sh <dataset|competition> <slug> <dest-name>}"
SLUG="${2:?missing slug}"
DEST_NAME="${3:?missing destination name}"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DEST="$REPO_ROOT/data/$DEST_NAME"

if ! command -v kaggle >/dev/null 2>&1; then
  echo "kaggle CLI not found. Install it with: pip install kaggle" >&2
  exit 1
fi

mkdir -p "$DEST"

case "$KIND" in
  dataset)
    kaggle datasets download -d "$SLUG" -p "$DEST" --unzip
    ;;
  competition)
    kaggle competitions download -c "$SLUG" -p "$DEST"
    (cd "$DEST" && unzip -o "*.zip" && rm -f *.zip)
    ;;
  *)
    echo "First argument must be 'dataset' or 'competition', got: $KIND" >&2
    exit 1
    ;;
esac

echo "Done. Files are in $DEST"
