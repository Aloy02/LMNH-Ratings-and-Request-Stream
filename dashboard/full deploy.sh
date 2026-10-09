#!/bin/bash
set -e

source ./config.sh.priv

echo "Starting deployment to EC2 Instance"

echo "Attempting to kill server"

ssh -o StrictHostKeyChecking=no -i .pem "${EC2_CONN}" "pkill -f pipeline.py" || true

echo "Killed server"

echo "Removing all files from EC2 Instance"

ssh -o "StrictHostKeyChecking=no" -i .pem "${EC2_CONN}" "rm -rf -- *"

echo "All files removed from EC2 Instance"

echo "Preparing to copy files to EC2 Instance"

scp -o "StrictHostKeyChecking=no" -i .pem -r ./* "${EC2_CONN}":.

scp -o "StrictHostKeyChecking=no" -i .pem -r .env "${EC2_CONN}":.

echo "Files copied to EC2 Instance"

echo "Starting SSH session to EC2 Instance"

ssh -o "StrictHostKeyChecking=no" -i .pem "${EC2_CONN}" < /dev/null << 'EOF'
    ls -a
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -r requirements.txt
    nohup python3 pipeline.py > app.log 2>&1 &
    exit
EOF

echo "SSH session ended"