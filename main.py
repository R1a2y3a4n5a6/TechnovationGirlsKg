import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Создай бота и вставь свой токен
bot = telebot.TeleBot("7575762615:AAEEYSGfM6RKjSQOMNoSIfzWIHxSr9m-A0s")

# Список вопросов и ответов
questions_answers = {
    "Как зарегистрироваться?": "Чтобы зарегистрироваться, перейдите по ссылке: https://technovationchallenge.org/",
    "Что такое Technovation?": "Technovation — это международная программа для девочек, где вы учитесь создавать мобильные приложения.",
    "Кто может участвовать?": "Девочки от 8 до 18 лет. Подробнее на сайте: https://technovationchallenge.org/"
}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    for question in questions_answers.keys():
        markup.add(InlineKeyboardButton(text=question, callback_data=question))
    bot.send_message(message.chat.id, "Привет! Выбери вопрос, чтобы получить ответ:", reply_markup=markup)

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    answer = questions_answers.get(call.data, "Извините, ответа на этот вопрос пока нет.")
    bot.send_message(call.message.chat.id, answer)

# Запуск бота
bot.polling(none_stop=True)
