<h1 align="center">Go2 Proprioceptive Terrain Locomotion</h1>

<p align="center">
  A single end-to-end Unitree Go2 locomotion pipeline: flat warm-start prior,
  rough-terrain training, stair fine-tuning, MuJoCo validation, and real-hardware deployment.
</p>

<p align="center">
  <a href="https://www.youtube.com/watch?v=oOYZdeQDaec">
    <img src="https://img.youtube.com/vi/oOYZdeQDaec/hqdefault.jpg" alt="Go2 terrain locomotion deployment video" width="720">
  </a>
</p>

<p align="center">
  <a href="docs/TRAINING.md">Training</a>
  ·
  <a href="docs/VALIDATION.md">Validation</a>
  ·
  <a href="docs/DEPLOYMENT.md">Deployment</a>
  ·
  <a href="docs/RUN_COMMANDS.md">Run commands</a>
</p>

This repository publishes one production pipeline only. Historical rough-only,
adaptation, C1, teacher/student, and ablation branches are intentionally not part
of this repo.

## Pipeline

```text
Stage 1: flat deployable prior
  -> Go2-Terrain-Flat-Prior-V1

Stage 2: rough/slopes terrain policy
  -> Go2-Terrain-Locomotion-Rough-V1

Stage 3: stairs and inverted-stairs fine-tune
  -> Go2-Terrain-Locomotion-Stairs-V1

Export
  -> TorchScript + ONNX + deploy_config.json + deploy.yaml

Validation
  -> bundle checks -> inference parity -> MuJoCo terrain suites -> Unitree MJLAB FSM audit

Deployment
  -> Unitree MJLAB C++ FSM -> DDS preflight -> FixStand -> Velocity policy
```

## Runtime Contract

The deployed actor is blind and proprioceptive. Privileged height scan, base
linear velocity, terrain, and dynamics information are critic-only during
training.

```text
policy_obs_dim      45
history_length     100
history_dim       4500
action_dim          12
control_dt        0.02 s
```

Actor observation order:

```text
base_ang_vel          3
projected_gravity    3
velocity_commands    3
joint_pos_rel       12
joint_vel_rel       12
last_action         12
```

Action semantics:

```text
target_joint_position = default_joint_position + 0.25 * policy_action
```

## Quick Start

```bash
export REPO=/path/to/go2-lab-rough-terrain-locomotion
export ISAACLAB_ROOT=/path/to/IsaacLab
cd "$REPO"
$ISAACLAB_ROOT/_isaac_sim/python.sh -m pip install --user --no-deps -e .

bash scripts/isaaclab_user.sh -p scripts/doctor_isaaclab.py
bash scripts/isaaclab_user.sh -p scripts/check_tasks.py
```

Train all stages:

```bash
bash scripts/isaaclab_user.sh -p scripts/train_flat_prior.py --headless \
  --log-dir ~/isaaclab_logs/go2_terrain_flat_prior_v1

bash scripts/isaaclab_user.sh -p scripts/train_terrain_policy.py --stage rough --headless \
  --flat-prior-checkpoint ~/isaaclab_logs/go2_terrain_flat_prior_v1/model_1499.pt \
  --log-dir ~/isaaclab_logs/go2_terrain_locomotion_rough_v1

bash scripts/isaaclab_user.sh -p scripts/train_terrain_policy.py --stage stairs --headless \
  --rough-checkpoint ~/isaaclab_logs/go2_terrain_locomotion_rough_v1/model_1999.pt \
  --log-dir ~/isaaclab_logs/go2_terrain_locomotion_stairs_v1
```

The default robot asset is expected at:

```text
assets/robots/go2/go2.usd
```

For a different Go2 USD, set:

```bash
export GO2_USD_PATH=/path/to/go2.usd
export GO2_BASE_BODY_NAME=base_link        # only if your asset uses base_link
export GO2_FOOT_BODY_REGEX='.*_calf'       # only if it has no *_foot bodies
export GO2_HEIGHT_SCANNER_PRIM='{ENV_REGEX_NS}/Robot/base_link'
```

## Docs

- `docs/TRAINING.md`: staged training from flat to rough to stairs.
- `docs/VALIDATION.md`: IsaacLab and MuJoCo validation gates.
- `docs/DEPLOYMENT.md`: export, runtime activation, DDS, and hardware bring-up.
- `docs/RUN_COMMANDS.md`: copy-paste command reference.
- `docs/DEPENDENCIES.md`: external dependencies and what is intentionally not vendored.
