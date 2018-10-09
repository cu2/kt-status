#!/bin/bash -e
set -o pipefail

PARENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )"

if [ ! -d "$PARENT_DIR/virtualenv" ]; then
  echo "Please run setup.sh first"
  exit 1
fi

. "$PARENT_DIR/virtualenv/bin/activate"

python "$PARENT_DIR/get_status.py"
