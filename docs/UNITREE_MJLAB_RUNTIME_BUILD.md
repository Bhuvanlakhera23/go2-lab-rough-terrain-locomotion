# Unitree MJLAB Runtime Build

The hardware deployment path uses the Unitree MJLAB C++ FSM runtime. This repo
owns the patch, staging, and validation flow; the external C++ repository remains
a local dependency.

## Setup

```bash
cd "$REPO"
git clone https://github.com/unitreerobotics/unitree_rl_mjlab.git reference_repos/unitree_rl_mjlab
cd reference_repos/unitree_rl_mjlab
git apply ../../patches/unitree_rl_mjlab/go2_scripted_controller.patch
cd "$REPO"
```

## Build

```bash
bash scripts/deploy/build_unitree_mjlab_runtime.sh all
```

## Stage Terrain Locomotion Bundle

```bash
export TERRAIN_BUNDLE=$REPO/artifacts/exported/go2_terrain_locomotion_steps_v1_candidate
bash scripts/deploy/run_unitree_mjlab_sim_deploy.sh activate
bash scripts/deploy/run_unitree_mjlab_sim_deploy.sh validate
```

The staged policy directory is:

```text
reference_repos/unitree_rl_mjlab/deploy/robots/go2/config/policy/velocity/go2_terrain_locomotion_steps_v1_candidate
```
