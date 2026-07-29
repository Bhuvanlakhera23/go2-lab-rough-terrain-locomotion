# Dependencies

This repo owns the Go2 terrain locomotion training, validation, export, and
bring-up code. Large external simulators and vendor SDKs are intentionally not
vendored.

## Required For Training

- Isaac Sim / IsaacLab
- IsaacLab-compatible `rsl_rl`
- Go2 USD asset at `assets/robots/go2/go2.usd` or via `GO2_USD_PATH`

Install this repo into Isaac Sim Python without dependency resolution:

```bash
$ISAACLAB_ROOT/_isaac_sim/python.sh -m pip install --user --no-deps -e .
```

Do not add or install arbitrary PyPI `torch` into Isaac Sim Python. IsaacLab owns
that CUDA/PyTorch stack.

## Required For MuJoCo Validation

- MuJoCo Python environment
- Go2 MuJoCo XML/scene path via `GO2_MUJOCO_MODEL`
- optional `reference_repos/unitree_mujoco` or MJLAB terrain tooling for terrain scenes

## Required For Unitree MJLAB FSM Runtime

- `reference_repos/unitree_rl_mjlab`
- `reference_repos/unitree_sdk2` or system Unitree SDK2 install
- C++ build dependencies: CMake, compiler, Eigen, Boost, yaml-cpp, fmt
- repo patch: `patches/unitree_rl_mjlab/go2_scripted_controller.patch`

## Required For Hardware DDS Diagnostics

- Python environment with `cyclonedds`
- `third_party/unitree_sdk2py` or `UNITREE_SDK2PY_ROOT` pointing to compatible Unitree SDK2 Python bindings

Generated logs, checkpoints, exported bundles, MuJoCo binaries, and validation
artifacts belong under `logs/` or `artifacts/` and are ignored by git.
