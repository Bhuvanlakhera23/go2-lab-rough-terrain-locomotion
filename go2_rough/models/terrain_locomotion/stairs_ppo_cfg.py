"""Runner config for the terrain locomotion stair baseline."""

from isaaclab.utils import configclass

from go2_rough.models.terrain_locomotion.rough_ppo_cfg import (
    Go2TerrainLocomotionRoughRunnerCfg,
    make_terrain_locomotion_policy,
)
from go2_rough.models.terrain_locomotion.stage_checkpoints import resolve_stage_checkpoint


@configclass
class Go2TerrainLocomotionStairsRunnerCfg(Go2TerrainLocomotionRoughRunnerCfg):
    """Stage 3: warm-start from the terrain rough checkpoint and fine-tune stairs."""

    max_iterations = 3000
    save_interval = 50
    experiment_name = "go2_terrain_locomotion_steps_v1"

    policy = make_terrain_locomotion_policy(
        actor_init_path=resolve_stage_checkpoint(
            ("TERRAIN_ROUGH_CKPT", "GO2_TERRAIN_ROUGH_CKPT"),
            "stairs-stage rough",
        )
    )

    
