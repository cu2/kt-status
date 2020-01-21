#!/bin/bash -e
set -o pipefail

PARENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )"

if [ ! -d "$PARENT_DIR/virtualenv" ]; then
  echo "Please run setup.sh first"
  exit 1
fi

. "$PARENT_DIR/virtualenv/bin/activate"

cd "$PARENT_DIR"

if [[ "$1" == "cloudwatch" ]]; then
  STATUS=$(python get_status.py)
  SUCCESS=$(echo "${STATUS}" | cut -d' ' -f2)
  RESPONSE_TIME=$(echo "${STATUS}" | cut -d' ' -f3)
  /usr/bin/aws cloudwatch put-metric-data --namespace KTStatus --metric-name Status --value "${SUCCESS}"
  /usr/bin/aws cloudwatch put-metric-data --namespace KTStatus --metric-name ResponseTime --value "${RESPONSE_TIME}" --unit Seconds
  echo "${STATUS}"
else
  python get_status.py
fi
