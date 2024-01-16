#!/bin/bash

if [ ! -d logs ]; then
  mkdir logs
fi

python3 -m venv .venv
source $venv_path/bin/activate
python3 -m pip install -r ./requirements.txt