import sqlite3


def create_db():
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()

    # Создаем таблицы
    cursor.execute('''CREATE TABLE IF NOT EXISTS sections (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
                        id INTEGER PRIMARY KEY,
                        question_text TEXT NOT NULL,
                        answer_text TEXT NOT NULL,
                        section_id INTEGER,
                        FOREIGN KEY (section_id) REFERENCES sections(id))''')

    conn.commit()
    conn.close()


def insert_data():
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()

    # Вставляем данные о секциях, если их ещё нет
    sections = [
        "Регистрация на сайте",
        "Командная работа",
        "Сроки проекта",
        "Учебные материалы. Curriculum",
        "Создание видео"
    ]

    for section in sections:
        cursor.execute("SELECT * FROM sections WHERE name=?", (section,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO sections (name) VALUES (?)", (section,))

    conn.commit()

    # Получаем id секций
    cursor.execute("SELECT id FROM sections WHERE name='Регистрация на сайте'")
    registration_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM sections WHERE name='Командная работа'")
    teamwork_id = cursor.fetchone()[0]

    # Вставляем вопросы и ответы
    questions_answers = [
        ("Что такое Technovation girls challenge?",
         "Technovation girls challenge — это бесплатная программа для девочек в возрасте от 8 до 18 лет, которая проводится ежегодно с октября по апрель. Работая в командах, девочки находят социальную проблему в своем обществе и создают мобильное приложение, чтобы помочь её решить.",
         registration_id),

        ("Как пройти регистрацию?",
         "Зайдите на сайт Technovation Girls и нажмите «Join Us». Выберите свою роль: участница, наставник, родитель или координатор. Заполните форму регистрации, указав необходимые данные. Найдите или соберите команду и приступайте к работе над проектом.",
         registration_id),

        ("Как зарегистрироваться участнику?",
         "Чтобы зарегистрироваться участнице Technovation Girls, зайдите на сайт, нажмите 'Join Us', выберите роль 'Student', создайте аккаунт, указав имя, возраст, страну и контакты, найдите или создайте команду с наставником и начните работу над проектом.",
         registration_id),

        ("Как зарегистрироваться ментору?",
         "Чтобы зарегистрироваться наставнику (Mentor) в Technovation Girls, зайдите на сайт, нажмите 'Join Us', выберите роль 'Mentor', создайте аккаунт, указав имя, страну и контактные данные, пройдите проверку и найдите команду для наставничества.",
         registration_id),

        ("Нужно ли создавать новый аккаунт для регистрации?",
         "Да, для каждой роли нужно создавать новый аккаунт. Выбирайте роль на сайте и регистрируйтесь.",
         registration_id),

        ("Как получить родительское соглашение?",
         "После регистрации участника на сайте Technovation Girls, родителю на электронную почту приходит уведомление о том, что его ребёнок зарегистрировался. В письме будет ссылка для подтверждения и подписания родительского соглашения.",
         registration_id),

        ("Когда дедлайн регистрации?",
         "Основной срок регистрации — 17 марта, но для вашего региона он до 10 февраля.",
         registration_id),

        ("Как создать команду?",
         "Чтобы создать или присоединиться к команде, нужно завершить регистрацию на сайте, перейти в профиль и выбрать опцию 'Создать свою команду' или 'Найти команду'.",
         teamwork_id),

        ("Как найти ментора?",
         "Найти ментора можно: 1) на сайте, отправив ему заявку; 2) пригласить своего знакомого старше 18 лет стать ментором; 3) написать человеку в соцсетях и предложить стать ментором.",
         teamwork_id),

        ("Можно ли участвовать без команды?",
         "Участвовать без команды нельзя, но можно, если в команде будет от 2 до 5 человек.",
         teamwork_id),

        ("Сколько менторов может быть в одной команде?",
         "Ограничений на количество менторов нет.",
         teamwork_id),

        ("Кто такой ментор?",
         "Ментор — это тот человек, который наставляет вас в течение проекта, даёт советы и помогает с определённой работой, например, анализировать ваш бизнес-план.",
         teamwork_id),

        ("Могут ли мои знакомые стать ментором?",
         "Да, конечно. Вы можете пригласить своих знакомых старше 18 лет стать вашим ментором.",
         teamwork_id),

        ("Можно ли работать с командой онлайн?",
         "Да, вы можете работать со своей командой онлайн, связываясь через Zoom, Google Meet и другие платформы, а также общаясь в письменном формате.",
         teamwork_id),

        ("Обязательно ли выбирать девочек, которые живут рядом?",
         "Нет, это не обязательно. Вы можете пригласить в свою команду девочек из других городов и регионов.",
         teamwork_id),

        ("Можно ли быть из разных регионов?",
         "Да, конечно.",
         teamwork_id)
    ]

    for question, answer, section_id in questions_answers:
        cursor.execute("SELECT * FROM questions WHERE question_text=?", (question,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO questions (question_text, answer_text, section_id) VALUES (?, ?, ?)",
                           (question, answer, section_id))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_db()
    insert_data()


