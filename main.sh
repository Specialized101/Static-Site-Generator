#!/bin/bash
python3 src/main.py "$1"
cd public && python3 -m http.server 8888