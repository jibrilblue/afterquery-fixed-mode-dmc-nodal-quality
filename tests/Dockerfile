FROM python:3.13-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5

COPY . /tests/
RUN mkdir -p /app/output

Test.sh

#!/usr/bin/env bash
set -uo pipefail

mkdir -p /logs/verifier
printf '0' > /logs/verifier/reward.txt

cd /tests
python -m pytest -q --ctrf /logs/verifier/ctrf.json test_dmc.py
status=$?

if [ "$status" -eq 0 ]; then
  printf '1' > /logs/verifier/reward.txt
else
  printf '0' > /logs/verifier/reward.txt
fi

exit 0
