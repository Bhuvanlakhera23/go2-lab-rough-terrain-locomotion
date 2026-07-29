"""Blind history environment with critic-only terrain and dynamics privilege."""

from __future__ import annotations

from isaaclab.sensors import RayCasterCfg, patterns
from isaaclab.utils import configclass

from go2_rough.envs.asset_contract import height_scanner_prim_path
from go2_rough.envs.privileged_obs import (
    DynamicsPrivilegedObsCfg,
    TerrainPrivilegedObsCfg,
    TrackedRandomizeRigidBodyMass,
    TrackedRandomizeRigidBodyMaterial,
)
from go2_rough.envs.terrain_locomotion.rough_history_base_cfg import Go2AsymPpoHistoryBaseEnvCfg


@configclass
class Go2TerrainPrivilegedHistoryEnvCfg(Go2AsymPpoHistoryBaseEnvCfg):
    """Blind history actor with terrain/dynamics signals restricted to critic."""

    policy_history_length: int = 100

    def __post_init__(self):
        super().__post_init__()

        self.scene.height_scanner = RayCasterCfg(
            prim_path=height_scanner_prim_path(),
            offset=RayCasterCfg.OffsetCfg(pos=(0.0, 0.0, 20.0)),
            ray_alignment="yaw",
            pattern_cfg=patterns.GridPatternCfg(resolution=0.1, size=[1.6, 1.0]),
            debug_vis=False,
            mesh_prim_paths=["/World/ground"],
        )
        self.scene.height_scanner.update_period = self.decimation * self.sim.dt

        self.observations.policy.height_scan = None
        self.events.physics_material.func = TrackedRandomizeRigidBodyMaterial
        if self.events.add_base_mass is not None:
            self.events.add_base_mass.func = TrackedRandomizeRigidBodyMass

        self.observations.terrain_privileged = TerrainPrivilegedObsCfg()
        self.observations.dynamics_privileged = DynamicsPrivilegedObsCfg()

        print("\n========== GO2 TERRAIN LOCOMOTION PRIVILEGED HISTORY ==========\n")
