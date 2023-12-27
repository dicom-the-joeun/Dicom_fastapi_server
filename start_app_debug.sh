#!/bin/bash
# start_app_debug.sh

cd "$(dirname "$0")"

source ./env/bin/activate

python -m uvicorn app.main:app --reload
