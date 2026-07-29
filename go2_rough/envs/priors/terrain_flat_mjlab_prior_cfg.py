"""Flat prior for the terrain locomotion branch."""

from __future__ import annotations

from isaaclab.utils import configclass

from go2_rough.envs.priors.flat_mjlab_prior_cfg import Go2FlatMjlabPriorEnvCfg


@configclass
class Go2TerrainFlatMjlabPriorEnvCfg(Go2FlatMjlabPriorEnvCfg):
    """Stage 1 flat prior under the deploy-honest MJLAB actor contract."""

    def __post_init__(self):
        super().__post_init__()
        print("\n========== GO2 TERRAIN FLAT MJLAB PRIOR V1 ==========\n")
