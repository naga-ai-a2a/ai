#!/usr/bin/env bash

if [ $# -ne 1 ]; then
    printf "\n\tNeed <model like openai:gpt-5.4> as arg\n\n"
    exit 9
fi

uv venv --clear >/dev/null 2>&1

source .venv/bin/activate

uv pip install -q -r Requirements.txt

python Weather.py $1 | jq
