@echo off
@title Updater Bot

rem Change directory to the script's directory
cd %~dp0

rem Activate the virtual environment
call venv\Scripts\activate.bat

rem Run your Python script
python bot.py

rem Deactivate the virtual environment
call venv\Scripts\deactivate.bat

echo.
echo Thanks for using Updater Bot
echo.

pause