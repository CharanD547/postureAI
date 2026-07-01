#!/usr/bin/env bash
# Run PostureAI with the project virtualenv (has opencv, mediapipe, etc.)
cd "$(dirname "$0")"
exec .venv/bin/streamlit run app.py "$@"
