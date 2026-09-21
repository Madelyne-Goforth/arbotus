#!/usr/bin/env bash
# Launches AR-BOTUS's web GUI. Activates the venv and starts the Flask
# server, regardless of what directory you run this script from.
set -e
cd "$(dirname "${BASH_SOURCE[0]}")"
source venv/bin/activate
python3 src/app.py
