#!/bin/bash
source .venv/bin/activate
cd src
python html_to_md.py
cd ..
