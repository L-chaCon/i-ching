#!/bin/bash

source_path=${1:-"static"}
content_path=${2:-"content"}
export SOURCE_PATH=$source_path
export CONTENT_PATH=$content_path
./.venv/bin/python src/main.py
cd public && ../.venv/bin/python -m http.server 42069
