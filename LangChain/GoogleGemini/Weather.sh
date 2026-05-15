#!/usr/bin/env bash

cd `dirname $0`

if [ $# -ne 2 ]; then
    printf "\n\tNeed <model like google_genai:gemini-2.5-flash-lite> <city like pune> as args\n\n"
    exit 9
fi

trap "rm -fr .venv" EXIT SIGINT SIGTERM

uv venv --clear >/dev/null 2>&1

source .venv/bin/activate

uv pip install -q -r Requirements.txt

python Weather.py $1 $2 | jq
