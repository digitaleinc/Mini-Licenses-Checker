@echo off
@title Uvicorn API Server by A.K.

rem Change directory to the script's directory
cd %~dp0

rem Activate the virtual environment
call venv\Scripts\uvicorn main:app --host 0.0.0.0 --port 6061

rem Run your Python script
python main.py

rem Deactivate the virtual environment
call venv\Scripts\deactivate.bat

echo.
echo Thanks for using A.K. software
echo.

pause