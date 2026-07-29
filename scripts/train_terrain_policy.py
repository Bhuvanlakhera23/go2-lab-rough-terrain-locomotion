#!/usr/bin/env python3
"""Train a stage of the Go2 proprioceptive terrain locomotion pipeline."""

from __future__ import annotations

import argparse
import os
import traceback
from pathlib import Path

from isaaclab.app import AppLauncher

TASK_BY_STAGE = {
    "rough": "Go2-Terrain-Locomotion-Rough-V1",
    "stairs": "Go2-Terrain-Locomotion-Stairs-V1",
}
DEFAULT_LOG_DIR_BY_STAGE = {
    "rough": "logs/go2_terrain_locomotion_rough_v1",
    "stairs": "logs/go2_terrain_locomotion_stairs_v1",
}

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--stage", choices=sorted(TASK_BY_STAGE), default="rough")
parser.add_argument("--task", default=None, help="Override the registered task for advanced use.")
parser.add_argument("--flat-prior-checkpoint", default=None, help="Stage-1 checkpoint used to warm-start rough training.")
parser.add_argument("--rough-checkpoint", default=None, help="Stage-2 checkpoint used to warm-start stair training.")
parser.add_argument("--num-envs", type=int, default=None)
parser.add_argument("--max-iterations", type=int, default=None)
parser.add_argument("--seed", type=int, default=42)
parser.add_argument("--log-dir", default=None)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()

if args_cli.flat_prior_checkpoint:
    os.environ["TERRAIN_FLAT_PRIOR_CKPT"] = args_cli.flat_prior_checkpoint
    os.environ["GO2_TERRAIN_FLAT_PRIOR_CKPT"] = args_cli.flat_prior_checkpoint
if args_cli.rough_checkpoint:
    os.environ["TERRAIN_ROUGH_CKPT"] = args_cli.rough_checkpoint
    os.environ["GO2_TERRAIN_ROUGH_CKPT"] = args_cli.rough_checkpoint

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import gymnasium as gym
from isaaclab_rl.rsl_rl import RslRlVecEnvWrapper
from isaaclab_tasks.utils.parse_cfg import load_cfg_from_registry
from rsl_rl.runners import OnPolicyRunner

import isaaclab_tasks  # noqa: F401
import go2_rough  # noqa: F401


def main() -> None:
    task = args_cli.task or TASK_BY_STAGE[args_cli.stage]
    log_dir = Path(args_cli.log_dir or DEFAULT_LOG_DIR_BY_STAGE[args_cli.stage]).expanduser()
    env_cfg = load_cfg_from_registry(task, "env_cfg_entry_point")
    runner_cfg = load_cfg_from_registry(task, "rsl_rl_cfg_entry_point")
    env_cfg.seed = int(args_cli.seed)
    if args_cli.num_envs is not None:
        env_cfg.scene.num_envs = int(args_cli.num_envs)
    if args_cli.max_iterations is not None:
        runner_cfg.max_iterations = int(args_cli.max_iterations)

    env_cfg.sim.log_dir = str(log_dir / "isaaclab")
    try:
        env = gym.make(task, cfg=env_cfg, render_mode=None)
    except Exception:
        print("[ERROR] Environment creation failed.")
        print(
            "[HINT] If your Go2 USD uses base_link and has no *_foot bodies, set "
            "GO2_BASE_BODY_NAME=base_link, GO2_FOOT_BODY_REGEX='.*_calf', and "
            "GO2_HEIGHT_SCANNER_PRIM='{ENV_REGEX_NS}/Robot/base_link'."
        )
        traceback.print_exc()
        raise
    env = RslRlVecEnvWrapper(env, clip_actions=runner_cfg.clip_actions)
    log_dir.mkdir(parents=True, exist_ok=True)
    runner = OnPolicyRunner(env, runner_cfg.to_dict(), log_dir=str(log_dir), device=runner_cfg.device)
    runner.learn(num_learning_iterations=runner_cfg.max_iterations)
    env.close()
    simulation_app.close()


if __name__ == "__main__":
    main()
