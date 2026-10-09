#!/bin/bash
set -e

source ./config.sh.priv

echo "Starting deployment to EC2 Instance"

echo "Attempting to kill server"

ssh -o StrictHostKeyChecking=no -i .pem "${EC2_CONN}" "pkill -f pipeline.py" || true

echo "Killed server"

echo "Reconnecting pipeline session"

ssh -o "StrictHostKeyChecking=no" -i .pem "${EC2_CONN}" < /dev/null << 'EOF'
    ls -a
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -r requirements.txt
    nohup python3 pipeline.py > app.log 2>&1 &
    exit
EOF

echo "Connection complete"