#!/bin/bash -e
set -o pipefail

PARENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )"

if [ ! -d "$PARENT_DIR/virtualenv" ]; then
  python3 -m venv "$PARENT_DIR/virtualenv"
fi

. "$PARENT_DIR/virtualenv/bin/activate"

pip install -q --upgrade pip
pip install -q --upgrade setuptools
pip install -q -r "$PARENT_DIR/requirements.txt"
