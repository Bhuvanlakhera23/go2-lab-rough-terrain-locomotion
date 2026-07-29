"""Runner config for the terrain locomotion flat prior stage."""

from isaaclab.utils import configclass

from go2_rough.models.priors.flat_mjlab_prior_runner_cfg import Go2FlatMjlabPriorPPORunnerCfg


@configclass
class Go2TerrainFlatMjlabPriorPPORunnerCfg(Go2FlatMjlabPriorPPORunnerCfg):
    """Stage 1: train a clean flat deployable actor for the production pipeline."""

    experiment_name = "go2_terrain_flat_mjlab_prior_v1"
