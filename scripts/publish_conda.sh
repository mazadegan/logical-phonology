#!/bin/bash
set -e
RECIPE_DIR=$(mktemp -d)
grayskull pypi logical-phonology --output "$RECIPE_DIR"
conda build "$RECIPE_DIR/logical-phonology" --no-anaconda-upload
anaconda upload -u mazadegan "$(conda build "$RECIPE_DIR/logical-phonology" --output)"
rm -rf "$RECIPE_DIR"
