#!/bin/bash
set -e
echo "Starting Interactive ML Model Explainer with Streamlit..."
uvicorn app:app --host 0.0.0.0 --port 9099 --workers 1
