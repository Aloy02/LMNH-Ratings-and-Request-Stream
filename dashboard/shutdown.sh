#!/bin/bash
set -e

source ./config.sh.priv

echo "Starting deployment to EC2 Instance"

echo "Attempting to kill server"

ssh -o StrictHostKeyChecking=no -i .pem "${EC2_CONN}" "pkill -f pipeline.py" || true

echo "Killed server"