# Training

The repository exposes one staged training pipeline.

## Stage 1: Flat Prior

Purpose: learn a clean deployable actor on flat ground under the same 45-D actor
observation contract used later by rough and stair stages.

```bash
bash scripts/isaaclab_user.sh -p scripts/train_flat_prior.py \
  --task Go2-Terrain-Flat-Prior-V1 \
  --headless \
  --log-dir ~/isaaclab_logs/go2_terrain_flat_prior_v1
```

## Stage 2: Rough / Slopes

Purpose: warm-start from the flat prior and train the blind history actor on
rough terrain, random rough patches, pyramid slopes, and inverted slopes.

```bash
bash scripts/isaaclab_user.sh -p scripts/train_terrain_policy.py \
  --stage rough \
  --flat-prior-checkpoint ~/isaaclab_logs/go2_terrain_flat_prior_v1/model_1499.pt \
  --headless \
  --log-dir ~/isaaclab_logs/go2_terrain_locomotion_rough_v1
```

## Stage 3: Stairs

Purpose: fine-tune the rough policy on stairs and inverted stairs only.

```bash
bash scripts/isaaclab_user.sh -p scripts/train_terrain_policy.py \
  --stage stairs \
  --rough-checkpoint ~/isaaclab_logs/go2_terrain_locomotion_rough_v1/model_1999.pt \
  --headless \
  --log-dir ~/isaaclab_logs/go2_terrain_locomotion_stairs_v1
```

## Core Randomization

- friction: static/dynamic randomized during training
- base mass: randomized during rough/stair stages
- motor stiffness and damping scale: `[0.6, 1.4]`
- pushes: enabled during rough/stair training
- actor: no base linear velocity, no height scan, no dynamics privilege
- critic: actor observations plus terrain/dynamics/base-linear-velocity privilege

Do not install repo dependencies into Isaac Sim Python with normal dependency
resolution. Use `pip install --user --no-deps -e .`; IsaacLab owns PyTorch and
CUDA compatibility.
