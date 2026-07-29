"""Checkpoint helpers for the staged terrain locomotion branch."""

from __future__ import annotations

import os
from pathlib import Path


def resolve_stage_checkpoint(env_names: tuple[str, ...], stage_name: str) -> str | None:
    """Resolve an explicit stage checkpoint from environment variables."""
    for env_name in env_names:
        candidate = os.environ.get(env_name)
        if candidate and Path(candidate).expanduser().is_file():
            resolved = str(Path(candidate).expanduser())
            print(f"[INFO] Terrain {stage_name} warm start: {resolved}")
            return resolved
    joined = ", ".join(env_names)
    print(f"[WARN] Terrain {stage_name} warm start not found. Set one of: {joined}")
    return None
