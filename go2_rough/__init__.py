"""Public task registry for the Go2 proprioceptive terrain locomotion pipeline."""

from __future__ import annotations

import gymnasium as gym
import rsl_rl.runners.on_policy_runner as _rsl_on_policy_runner

from go2_rough.models.terrain_locomotion.history_actor_critic import TemporalBlindActorCritic


_rsl_on_policy_runner.TemporalBlindActorCritic = TemporalBlindActorCritic


def _register_task(task_id: str, env_cfg_entry_point: str, rsl_rl_cfg_entry_point: str) -> None:
    gym.register(
        id=task_id,
        entry_point="isaaclab.envs:ManagerBasedRLEnv",
        kwargs={
            "env_cfg_entry_point": env_cfg_entry_point,
            "rsl_rl_cfg_entry_point": rsl_rl_cfg_entry_point,
        },
    )


_register_task(
    "Go2-Terrain-Flat-Prior-V1",
    "go2_rough.envs.priors.terrain_flat_mjlab_prior_cfg:Go2TerrainFlatMjlabPriorEnvCfg",
    "go2_rough.models.priors.terrain_flat_mjlab_prior_runner_cfg:Go2TerrainFlatMjlabPriorPPORunnerCfg",
)

_register_task(
    "Go2-Terrain-Locomotion-Rough-V1",
    "go2_rough.envs.terrain_locomotion.rough_mjlab_cfg:Go2TerrainLocomotionRoughEnvCfg",
    "go2_rough.models.terrain_locomotion.rough_ppo_cfg:Go2TerrainLocomotionRoughRunnerCfg",
)

_register_task(
    "Go2-Terrain-Locomotion-Stairs-V1",
    "go2_rough.envs.terrain_locomotion.stairs_mjlab_cfg:Go2TerrainLocomotionStairsEnvCfg",
    "go2_rough.models.terrain_locomotion.stairs_ppo_cfg:Go2TerrainLocomotionStairsRunnerCfg",
)
