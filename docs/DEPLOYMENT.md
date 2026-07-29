# Deployment

Deployment uses an exported bundle and the Unitree MJLAB C++ FSM runtime.

## Export

```bash
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

## Hardware Gate

1. `dds-probe ethernet`
2. activate/stage runtime
3. validate FSM runtime
4. FixStand on robot
5. low-speed Velocity policy
6. monitor LowState/LowCmd
7. terrain/stair bring-up only after flat walking is stable

```bash
bash scripts/deploy/run_unitree_mjlab_sim_deploy.sh activate
bash scripts/deploy/run_unitree_mjlab_sim_deploy.sh validate
bash scripts/deploy/run_unitree_mjlab_sim_deploy.sh dds-probe ethernet
bash scripts/deploy/run_unitree_mjlab_sim_deploy.sh hardware ethernet
```
