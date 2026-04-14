#!/bin/bash
set -e
python scripts/bump_version.py
python scripts/make_api_reference.py
rm -rf dist/
python -m build
twine upload dist/*
python scripts/tag_release.py
git add -A
git commit -m "version bump"
git push origin main
