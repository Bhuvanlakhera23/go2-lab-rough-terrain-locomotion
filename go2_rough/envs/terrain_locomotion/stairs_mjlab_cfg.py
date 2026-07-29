"""Go2 terrain locomotion stair fine-tune stage.

Stage 3 of the production pipeline fine-tunes the rough-stage policy on stairs-only
terrain.


"""

from __future__ import annotations

from isaaclab.utils import configclass

from go2_rough.envs.terrain_locomotion.rough_mjlab_cfg import (
    Go2TerrainLocomotionRoughEnvCfg,
)


@configclass
class Go2TerrainLocomotionStairsEnvCfg(Go2TerrainLocomotionRoughEnvCfg):
    """Stage 3: rough policy fine-tuned on stairs and inverted stairs."""

    def __post_init__(self):
        super().__post_init__()

        terrain_gen = self.scene.terrain.terrain_generator
        self.scene.terrain.max_init_terrain_level = 1
        terrain_gen.sub_terrains["random_rough"].proportion = 0.0
        terrain_gen.sub_terrains["hf_pyramid_slope"].proportion = 0.0
        terrain_gen.sub_terrains["hf_pyramid_slope_inv"].proportion = 0.0
        terrain_gen.sub_terrains["pyramid_stairs"].proportion = 0.5
        terrain_gen.sub_terrains["pyramid_stairs_inv"].proportion = 0.5
        terrain_gen.sub_terrains["boxes"].proportion = 0.0

        for terrain_name in ("pyramid_stairs", "pyramid_stairs_inv"):
            terrain_cfg = terrain_gen.sub_terrains[terrain_name]
            terrain_cfg.step_height_range = (0.12, 0.12)
            terrain_cfg.step_width = 0.30
            terrain_cfg.platform_width = 3.0
        

        self.rewards.feet_air_time.weight = 0.5
        self.rewards.lin_vel_z_l2.weight = -0.5
        self.rewards.stable_progress.weight = 0.5
        self.rewards.adaptive_swing_recovery.weight = 0.25

        print("\n========== GO2 TERRAIN LOCOMOTION STAIRS V1 ==========\n")
