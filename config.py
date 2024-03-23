import sqlite3
import telebot


bot = telebot.TeleBot("YOUR_BOT_TOKEN_HERE")

# DB
connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = connection.cursor()

admins = ['user_id_1', 'user_id_2']
