#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cat <<EOF2
[INFO] Public training repo: ${REPO_ROOT}

Expected flow:
  1. Train flat, rough, and stair stages.
  2. Export go2_terrain_locomotion_steps_v1_candidate.
  3. Run deployment validation gate.
  4. Run MuJoCo sim2sim.
  5. Stage the Unitree MJLAB C++ FSM runtime.
  6. Probe DDS before hardware.

Core commands:

  cd "${REPO_ROOT}"
  bash scripts/deploy/run_unitree_mjlab_sim_deploy.sh activate
  bash scripts/deploy/run_unitree_mjlab_sim_deploy.sh validate
  bash scripts/deploy/run_unitree_mjlab_sim_deploy.sh controller
  bash scripts/deploy/run_unitree_mjlab_sim_deploy.sh sim

Hardware:

  bash scripts/deploy/run_unitree_mjlab_sim_deploy.sh dds-probe ethernet
  bash scripts/deploy/run_unitree_mjlab_sim_deploy.sh hardware ethernet

See:
  docs/RUN_COMMANDS.md
  docs/DEPLOYMENT.md
  docs/UNITREE_MJLAB_RUNTIME_BUILD.md
EOF2
