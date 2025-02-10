#!/bin/bash

PYTHONPATH=$(pwd)/src
export PYTHONPATH=$PYTHONPATH

mkdir -p logs

# Start FastAPI
uvicorn app.main:app --reload --host localhost --port 8000 2>&1 | tee logs/fastapi.log &

# Start Streamlit
streamlit run src/streamlit_app/main.py --server.port 8501 --server.address localhost 2>&1 | tee logs/streamlit.log &

wait
