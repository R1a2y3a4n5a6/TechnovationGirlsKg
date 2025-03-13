import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import sqlite3

bot = telebot.TeleBot(os.getenv("7575762615:AAEEYSGfM6RKjSQOMNoSIfzWIHxSr9m-A0s"))

import sqlite3

def get_questions():
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute("SELECT question_text, answer_text FROM questions")
    questions = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return questions

questions_answers = get_questions()

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    for question in questions_answers.keys():
        markup.add(InlineKeyboardButton(text=question, callback_data=question))
    bot.send_message(message.chat.id, "Привет! Выбери вопрос, чтобы получить ответ:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    answer = questions_answers.get(call.data, "Извините, ответа на этот вопрос пока нет.")
    bot.send_message(call.message.chat.id, answer)

bot.polling(none_stop=True)