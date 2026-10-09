#!/bin/bash
set -e

source ./config.sh.priv

ssh -o "StrictHostKeyChecking=no" -i .pem "${EC2_CONN}"