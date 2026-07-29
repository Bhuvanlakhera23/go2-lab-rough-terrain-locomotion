#!/usr/bin/env python3
"""Sanity-check that the production Gym tasks register correctly."""

from __future__ import annotations

import gymnasium as gym

import go2_rough  # noqa: F401


TASKS = [
    "Go2-Terrain-Flat-Prior-V1",
    "Go2-Terrain-Locomotion-Rough-V1",
    "Go2-Terrain-Locomotion-Stairs-V1",
]


def main() -> None:
    for task_id in TASKS:
        print(gym.spec(task_id).id)


if __name__ == "__main__":
    main()
