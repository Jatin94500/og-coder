@echo off
echo ========================================
echo Space Weather Dashboard
echo ========================================
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting dashboard...
echo.
echo Dashboard will open at: http://localhost:8501
echo Press Ctrl+C to stop
echo.
streamlit run app.py
