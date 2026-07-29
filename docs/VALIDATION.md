# Validation

A candidate is not considered deployable until it passes all structural and
simulator gates.

## Bundle Gate

```bash
python scripts/deploy/run_deployment_validation_gate.py \
  --bundle-dir "$TERRAIN_BUNDLE" \
  --expected-policy-obs-dim 45 \
  --expected-history-length 100 \
  --expected-action-dim 12 \
  --model-path "$GO2_MUJOCO_MODEL"
```

This checks bundle structure, tensor contract, TorchScript forward pass,
TorchScript/ONNX parity, MuJoCo preflight, and Unitree MJLAB FSM config.

## MuJoCo Terrain Suites

```bash
bash scripts/deploy/run_terrain_locomotion_model5099_mujoco_validation.sh
```

The suite records survival, falls, body height, tilt, velocity/yaw error,
control saturation, and non-foot terrain contact anomalies.
