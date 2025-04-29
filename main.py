import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

bot = telebot.TeleBot("7746129266:AAHR6xOsvcHlK50RV13fhhfsYc4Vxp-J_aI")


# Получение данных о секциях
def get_sections():
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, section_name FROM sections")
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


# Получение section_id по question_id
def get_section_id_by_question(question_id):
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute("SELECT section_id FROM questions WHERE id=?", (question_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


@bot.message_handler(commands=['start'])
def start(message):
    # Сначала отправляем красивое приветственное сообщение
    bot.send_message(
        message.chat.id,
        "👋 Привет! Мы — команда Technovation Girls Кыргызстан!\n\n"
        "Technovation — это международная программа для девочек 8-18 лет, "
        "которая учит создавать мобильные приложения для решения социальных проблем.\n\n"
        "Я здесь, чтобы помочь тебе с любыми вопросами о программе! 📚✨\n"
        "Выбирай интересующую тему ниже, и я всё объясню. 😉"
    )

    send_sections(message.chat.id)


def send_sections(chat_id):
    sections = get_sections()

    if not sections:
        bot.send_message(chat_id, "Извините, данные временно недоступны.")
        return

    markup = InlineKeyboardMarkup()
    for section_id, section_name in sections:
        markup.add(InlineKeyboardButton(text=section_name, callback_data=f"section_{section_id}"))

    bot.send_message(chat_id, "👇 Выбери интересующую тему:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("section_"))
def show_questions(call):
    section_id = int(call.data.split("_")[1])
    questions = get_questions_by_section(section_id)

    if not questions:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Извините, вопросов в этой секции пока нет."
        )
        return

    markup = InlineKeyboardMarkup()
    for question_id, question_text in questions:
        markup.add(InlineKeyboardButton(text=question_text, callback_data=f"question_{question_id}"))
    markup.add(InlineKeyboardButton(text="🔙 Назад к секциям", callback_data="back_to_sections"))

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="👇 Выбери вопрос:",
        reply_markup=markup
    )

def get_answer_and_file(question_id):
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute("SELECT answer_text, file_path FROM questions WHERE id=?", (question_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0], result[1]  # answer_text, file_path
    else:
        return "Извините, ответа на этот вопрос пока нет.", None


@bot.callback_query_handler(func=lambda call: call.data.startswith("question_"))
def show_answer(call):
    question_id = int(call.data.split("_")[1])
    answer, file_path = get_answer_and_file(question_id)

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="🔙 Назад к вопросам", callback_data=f"back_to_questions_{question_id}"))
    markup.add(InlineKeyboardButton(text="🏠 В главное меню", callback_data="back_to_sections"))

    # Сначала отправляем текст ответа
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=answer,
        reply_markup=markup
    )

    # Потом, если файл есть, отправляем файл
    if file_path:
        try:
            with open(file_path, 'rb') as f:
                bot.send_document(call.message.chat.id, f)
        except Exception as e:
            bot.send_message(call.message.chat.id, "⚠️ Не удалось отправить файл. Возможно, он отсутствует на сервере.")



@bot.callback_query_handler(func=lambda call: call.data == "back_to_sections")
def back_to_sections(call):
    sections = get_sections()

    if not sections:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Извините, данные временно недоступны."
        )
        return

    markup = InlineKeyboardMarkup()
    for section_id, section_name in sections:
        markup.add(InlineKeyboardButton(text=section_name, callback_data=f"section_{section_id}"))

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="👇 Выбери интересующую тему:",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("back_to_questions_"))
def back_to_questions(call):
    question_id = int(call.data.split("_")[-1])
    section_id = get_section_id_by_question(question_id)

    questions = get_questions_by_section(section_id)

    markup = InlineKeyboardMarkup()
    for q_id, question_text in questions:
        markup.add(InlineKeyboardButton(text=question_text, callback_data=f"question_{q_id}"))
    markup.add(InlineKeyboardButton(text="🔙 Назад к секциям", callback_data="back_to_sections"))

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="👇 Выбери вопрос:",
        reply_markup=markup
    )


bot.polling(none_stop=True)
