#!/bin/bash

cwd=$(realpath ./)
venv_path=$cwd/.venv
python_version=$(python3 --version | sed -r 's/\.[0-9]+$//g' | sed -r 's/\ //g' | tr '[:upper:]' '[:lower:]')
venv_packages=$venv_path/lib/$python_version/site-packages
python_packages=/usr/lib/$python_version
dist_packages=/usr/lib/python3/dist-packages

echo "Activating virtual environment..." && \
python3 -m venv $venv_path && \
source $venv_path/bin/activate && \

echo "Installing requirements..." && \
python3 -m pip install -r $cwd/requirements.txt && \

echo "Setting up installer..." && \
pyinstaller \
  --noconfirm \
  --onefile \
  --name "blood-emporium" \
  --paths $cwd:$venv_packages:$venv_path:$python_packages:$dist_packages \
  --add-data $venv_packages/ultralytics:ultralytics \
  --add-data assets:assets \
  --add-data backend:backend \
  --add-data frontend:frontend \
  $cwd/main.py && \

echo "Starting build..." && \
pyinstaller \
  --noconfirm \
  --distpath $(realpath ./dist) \
  $cwd/blood-emporium.spec