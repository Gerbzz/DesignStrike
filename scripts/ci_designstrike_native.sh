#!/usr/bin/env bash
set -euo pipefail

# Run only under Xvfb on the temporary public standard runner. All documents
# are synthetic, generated inside this source workspace, and stored in RUNNER_TEMP.
app="$1"
out="$2"
mkdir -p "$out"
export DESIGNCRAFT_CONFIG_DIR="$out/profile"
export WGPU_BACKEND=gl
export LIBGL_ALWAYS_SOFTWARE=1
export RUST_BACKTRACE=1
"$app" --control 18950 >"$out/desktop.log" 2>&1 &
app_pid=$!
trap 'kill "$app_pid" 2>/dev/null || true; wait "$app_pid" 2>/dev/null || true' EXIT

python3 scripts/ci_designstrike_native.py "$out" "$app_pid"
