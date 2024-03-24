[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct.svg)](https://vshymanskyy.github.io/StandWithUkraine)

# Mini-Licenses-Checker
This project is a simply-made and scalable backend API for updating your Python projects.
Front End is made via Telegram Bot for easy configuration.
Back End is made with FastAPI

## Advantages:
1. Fast and easy installation
2. Scalable
3. Convenient configuration in real time via Telegram Bot

## Installation for Windows (For linux later):
1. Clone the repository
2. Start installation.bat script. It will create venv automatically and install all the libraries for usage
3. Configure config.py file
4. If you want to change port of Back-end API: change 8th line of start_server.bat file to any port you need:
```
call venv\Scripts\uvicorn main:app --host 0.0.0.0 --port your_port
```
5. Start the start_bot.bat and start_server.bat

## You're ready to go!
