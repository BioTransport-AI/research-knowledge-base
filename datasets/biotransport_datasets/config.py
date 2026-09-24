"""Loads datasets.yaml into simple, typed lookups. No pandas/torch dependency here
on purpose -- this module should stay importable with nothing but PyYAML installed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = REPO_ROOT / "datasets" / "datasets.yaml"


@dataclass(frozen=True)
class DatasetSpec:
    name: str
    condition: str
    modality: list[str]
    access: str
    license: str
    local_dir: Path | None
    recipe: str | None
    kaggle_slug: str | None = None
    notes: str = ""

    @property
    def index_path(self) -> Path:
        """Where build_index() writes/reads this dataset's Parquet index."""
        if self.local_dir is None:
            raise ValueError(f"{self.name} has no local_dir (queried live, not indexed)")
        return REPO_ROOT / self.local_dir / "index.parquet"

    @property
    def raw_dir(self) -> Path:
        if self.local_dir is None:
            raise ValueError(f"{self.name} has no local_dir (queried live, not indexed)")
        return REPO_ROOT / self.local_dir


def _load_registry() -> dict[str, DatasetSpec]:
    with open(REGISTRY_PATH) as f:
        raw = yaml.safe_load(f)
    specs: dict[str, DatasetSpec] = {}
    for entry in raw["datasets"]:
        local_dir = entry.get("local_dir")
        specs[entry["name"]] = DatasetSpec(
            name=entry["name"],
            condition=entry["condition"],
            modality=entry.get("modality", []),
            access=entry["access"],
            license=entry.get("license", "unspecified"),
            local_dir=Path(local_dir) if local_dir else None,
            recipe=entry.get("recipe"),
            kaggle_slug=entry.get("kaggle_slug"),
            notes=entry.get("notes", "").strip(),
        )
    return specs


_REGISTRY: dict[str, DatasetSpec] | None = None


def registry() -> dict[str, DatasetSpec]:
    """Lazily-loaded, cached view of datasets.yaml. Call again after editing the
    YAML in the same process (e.g. a notebook) via `reload_registry()`.
    """
    global _REGISTRY
    if _REGISTRY is None:
        _REGISTRY = _load_registry()
    return _REGISTRY


def reload_registry() -> dict[str, DatasetSpec]:
    global _REGISTRY
    _REGISTRY = _load_registry()
    return _REGISTRY


def get_spec(name: str) -> DatasetSpec:
    try:
        return registry()[name]
    except KeyError as e:
        available = ", ".join(sorted(registry()))
        raise KeyError(f"Unknown dataset {name!r}. Available: {available}") from e


def with_recipe() -> list[DatasetSpec]:
    """Datasets that currently have an indexing recipe implemented."""
    return [s for s in registry().values() if s.recipe]
