:: UNTESTED (I don't have Windows to test this)

@echo off

set PYTHONPATH=%cd%\src
echo PYTHONPATH is set to: %PYTHONPATH%

if not exist logs (
    mkdir logs
)

:: Start FastAPI
start "" uvicorn app.main:app --reload --host localhost --port 8000 >> logs\fastapi.log 2>&1

:: Start Streamlit
start "" streamlit run src\streamlit_app\main.py --server.port 8501 --server.address localhost >> logs\streamlit.log 2>&1

pause
