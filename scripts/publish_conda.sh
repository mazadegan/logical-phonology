#!/bin/bash
set -e

log() {
  echo "==> $1"
}

RECIPE_DIR=$(mktemp -d)
trap 'rm -rf "$RECIPE_DIR"' EXIT

log "Checking grayskull"
if ! grayskull --version >/dev/null 2>&1; then
  echo "grayskull is not available in the current environment." >&2
  exit 1
fi

log "Checking conda-build"
if ! conda-build --version >/dev/null 2>&1; then
  echo "conda-build is not available in the current environment." >&2
  exit 1
fi

log "Generating recipe from PyPI"
grayskull pypi logical-phonology --output "$RECIPE_DIR"

log "Building conda package"
conda-build "$RECIPE_DIR/logical-phonology" --no-anaconda-upload

log "Resolving built package path"
PACKAGE_PATH=$(conda-build "$RECIPE_DIR/logical-phonology" --output | tail -n 1)

log "Uploading $PACKAGE_PATH"
anaconda upload -u mazadegan "$PACKAGE_PATH"
