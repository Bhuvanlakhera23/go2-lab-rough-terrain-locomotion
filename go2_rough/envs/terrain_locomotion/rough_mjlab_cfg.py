"""Go2 terrain locomotion rough stage.

Stage 2 of the production pipeline trains on rough terrain after the branch-specific
flat prior is learned.  This task intentionally keeps stairs disabled; stairs
belong to Stage 3.
"""

from __future__ import annotations

from isaaclab.managers import EventTermCfg
from isaaclab.managers import SceneEntityCfg
from isaaclab.utils import configclass
import isaaclab_tasks.manager_based.locomotion.velocity.mdp as mdp

from go2_rough.envs.asset_contract import base_body_name
from go2_rough.envs.terrain_locomotion.rough_omni_cfg import Go2AsymPpoRoughOmniEnvCfg
from go2_rough.envs.mjlab_contract import MjlabCriticPrivilegedObsCfg, apply_mjlab_policy_contract


@configclass
class Go2TerrainLocomotionRoughEnvCfg(Go2AsymPpoRoughOmniEnvCfg):
    """Stage 2: rough/slopes terrain locomotion without stair exposure."""

    mjlab_use_gait_phase: bool = False

    def __post_init__(self):
        super().__post_init__()

        apply_mjlab_policy_contract(
            self.observations.policy,
            include_gait_phase=self.mjlab_use_gait_phase,
        )
        apply_mjlab_policy_contract(
            self.observations.policy_history,
            include_gait_phase=self.mjlab_use_gait_phase,
        )
        self.observations.critic_privileged = MjlabCriticPrivilegedObsCfg()

        self.events.motor_strength.params["stiffness_distribution_params"] = (0.6, 1.4)
        self.events.motor_strength.params["damping_distribution_params"] = (0.6, 1.4)

        self.events.push_robot = EventTermCfg(
            func=mdp.push_by_setting_velocity,
            mode="interval",
            interval_range_s=(6.0, 10.0),
            params={
                "asset_cfg": SceneEntityCfg("robot"),
                "velocity_range": {
                    "x": (-0.35, 0.35),
                    "y": (-0.35, 0.35),
                    "yaw": (-0.4, 0.4),
                },
            },
        )
        self.events.base_com = EventTermCfg(
            func=mdp.randomize_rigid_body_com,
            mode="startup",
            params={
                "asset_cfg": SceneEntityCfg("robot", body_names=base_body_name()),
                "com_range": {
                    "x": (-0.03, 0.03),
                    "y": (-0.03, 0.03),
                    "z": (-0.01, 0.01),
                },
            },
        )

        self.scene.num_envs = 2048

        cmd = self.commands.base_velocity
        cmd.ranges.lin_vel_x = (-0.1, 0.1)
        cmd.ranges.lin_vel_y = (-0.1, 0.1)
        cmd.ranges.ang_vel_z = (-0.1, 0.1)
        cmd.limit_ranges.lin_vel_x = (-0.8, 0.8)
        cmd.limit_ranges.lin_vel_y = (-0.3, 0.3)
        cmd.limit_ranges.ang_vel_z = (-0.6, 0.6)

        terrain_gen = self.scene.terrain.terrain_generator
        self.scene.terrain.max_init_terrain_level = 2
        terrain_gen.sub_terrains["random_rough"].proportion = 0.35
        terrain_gen.sub_terrains["hf_pyramid_slope"].proportion = 0.15
        terrain_gen.sub_terrains["hf_pyramid_slope_inv"].proportion = 0.15
        terrain_gen.sub_terrains["pyramid_stairs"].proportion = 0.0
        terrain_gen.sub_terrains["pyramid_stairs_inv"].proportion = 0.0
        terrain_gen.sub_terrains["boxes"].proportion = 0.0

        self.rewards.track_lin_vel_xy_exp.weight = 2.0
        self.rewards.stable_progress.weight = 0.75
        self.rewards.adaptive_swing_recovery.weight = 0.0

        print("\n========== GO2 TERRAIN LOCOMOTION ROUGH V1 ==========\n")
