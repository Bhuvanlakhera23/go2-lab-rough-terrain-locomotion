# Reproduction

This is the full public reproduction flow for the single production pipeline.

## 1. Install

```bash
export REPO=/path/to/go2-lab-rough-terrain-locomotion
export ISAACLAB_ROOT=/path/to/IsaacLab
cd "$REPO"
$ISAACLAB_ROOT/_isaac_sim/python.sh -m pip install --user --no-deps -e .

bash scripts/isaaclab_user.sh -p scripts/doctor_isaaclab.py
bash scripts/isaaclab_user.sh -p scripts/check_tasks.py
```

## 2. Train

```bash
bash scripts/isaaclab_user.sh -p scripts/train_flat_prior.py \
  --task Go2-Terrain-Flat-Prior-V1 \
  --headless \
  --log-dir ~/isaaclab_logs/go2_terrain_flat_prior_v1

bash scripts/isaaclab_user.sh -p scripts/train_terrain_policy.py \
  --stage rough \
  --flat-prior-checkpoint ~/isaaclab_logs/go2_terrain_flat_prior_v1/model_1499.pt \
  --headless \
  --log-dir ~/isaaclab_logs/go2_terrain_locomotion_rough_v1

bash scripts/isaaclab_user.sh -p scripts/train_terrain_policy.py \
  --stage stairs \
  --rough-checkpoint ~/isaaclab_logs/go2_terrain_locomotion_rough_v1/model_1999.pt \
  --headless \
  --log-dir ~/isaaclab_logs/go2_terrain_locomotion_stairs_v1
```

## 3. Export

```bash
export TERRAIN_STEPS_CKPT=~/isaaclab_logs/go2_terrain_locomotion_stairs_v1/model_2999.pt
export TERRAIN_BUNDLE=$REPO/artifacts/exported/go2_terrain_locomotion_steps_v1_candidate

bash scripts/isaaclab_user.sh -p scripts/deploy/export_policy.py \
  --policy-name go2_terrain_locomotion_steps_v1_candidate \
  --checkpoint "$TERRAIN_STEPS_CKPT" \
  --task Go2-Terrain-Locomotion-Stairs-V1 \
  --phase terrain-locomotion-stairs-v1 \
  --bundle-dir "$TERRAIN_BUNDLE" \
  --policy-kind blind_history_policy \
  --observation-groups policy,policy_history \
  --policy-history-length 100 \
  --command-lin-vel-x -0.8 0.8 \
  --command-lin-vel-y -0.3 0.3 \
  --command-ang-vel-z -0.6 0.6 \
  --format torchscript \
  --format onnx
```

## 4. Validate

```bash
export GO2_MUJOCO_MODEL=/path/to/unitree_go2/scene.xml
python scripts/deploy/run_deployment_validation_gate.py \
  --bundle-dir "$TERRAIN_BUNDLE" \
  --expected-policy-obs-dim 45 \
  --expected-history-length 100 \
  --expected-action-dim 12 \
  --model-path "$GO2_MUJOCO_MODEL"
```

## 5. Deploy

```bash
bash scripts/deploy/run_unitree_mjlab_sim_deploy.sh activate
bash scripts/deploy/run_unitree_mjlab_sim_deploy.sh validate
bash scripts/deploy/run_unitree_mjlab_sim_deploy.sh dds-probe ethernet
bash scripts/deploy/run_unitree_mjlab_sim_deploy.sh hardware ethernet
```
