#!/usr/bin/env bash
set -euo pipefail

start_time=$(date +%s -d '15 min ago')
end_time=$(date +%s)

function get_and_send_metric() {
  metric_name="$1"
  start_time="$2"
  end_time="$3"

  value=$(/usr/local/bin/aws lightsail get-instance-metric-data \
    --instance-name marvin-iii-server \
    --metric-name "${metric_name}" \
    --period 300 \
    --start-time "${start_time}" \
    --end-time "${end_time}" \
    --unit Percent \
    --statistics Average \
    --region eu-central-1 \
    --query 'metricData[0].average')

  /usr/local/bin/aws cloudwatch put-metric-data \
    --namespace KTStatus \
    --timestamp "${start_time}" \
    --metric-name "${metric_name}" \
    --value "${value}" \
    --unit Percent

  echo "${metric_name}=${value}"
}

get_and_send_metric CPUUtilization "${start_time}" "${end_time}"
get_and_send_metric BurstCapacityPercentage "${start_time}" "${end_time}"
