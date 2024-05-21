#!/bin/bash

cd "$(dirname "$0")" || exit 1

if [[ ! -d .venv ]]; then
  python -m venv .venv
fi

source .venv/bin/activate
pip install --upgrade build
pip install --upgrade black
pip install --upgrade pytest

if ! python -m black --check ./*.py ./**/*.py; then
  echo "black failed"
  exit 1
fi

if ! pytest tests/*; then
  echo "pytest failed!"
  exit 1
fi

rm -rf dist

python -m build
