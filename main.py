import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

bot = telebot.TeleBot("7544500117:AAHF5K2iilzTfq8zr9K9jzBIKle4co_VE9A")


# Получение данных о секциях
def get_sections():
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM sections")
    sections = cursor.fetchall()
    conn.close()
    return sections


# Получение вопросов по id секции
def get_questions_by_section(section_id):
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, question_text FROM questions WHERE section_id=?", (section_id,))
    questions = cursor.fetchall()
    conn.close()
    return questions


# Получение ответа по id вопроса
def get_answer(question_id):
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute("SELECT answer_text FROM questions WHERE id=?", (question_id,))
    answer = cursor.fetchone()
    conn.close()
    return answer[0] if answer else "Извините, ответа на этот вопрос пока нет."


@bot.message_handler(commands=['start'])
def start(message):
    sections = get_sections()

    if not sections:
        bot.send_message(message.chat.id, "Извините, данные временно недоступны.")
        return

    markup = InlineKeyboardMarkup()
    for section_id, section_name in sections:
        markup.add(InlineKeyboardButton(text=section_name, callback_data=f"section_{section_id}"))

    bot.send_message(message.chat.id, "Привет! Выбери секцию:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("section_"))
def show_questions(call):
    section_id = int(call.data.split("_")[1])
    questions = get_questions_by_section(section_id)

    if not questions:
        bot.send_message(call.message.chat.id, "Извините, вопросов в этой секции пока нет.")
        return

    markup = InlineKeyboardMarkup()
    for question_id, question_text in questions:
        markup.add(InlineKeyboardButton(text=question_text, callback_data=f"question_{question_id}"))

    bot.send_message(call.message.chat.id, "Выбери вопрос:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("question_"))
def show_answer(call):
    question_id = int(call.data.split("_")[1])
    answer = get_answer(question_id)
    bot.send_message(call.message.chat.id, answer)


bot.polling(none_stop=True)