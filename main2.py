import sqlite3
from sqlite3 import Error
import re
import time

task = """"Поправить все на pep8 по возможности 
"""
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_users_table():
    database = r'C:\Users\я\PycharmProjects\pythonProject3\quiz_users.sqlite'
    conn = create_connection(database)
    c = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL,
    password TEXT NOT NULL,
    safeword TEXT NOT NULL,
    email TEXT NOT NULL); """ # sql запрос на построение таблицы
    try:
        c.execute(query)
        conn.commit()
        conn.close()
        print('executed')
        time.sleep(1)
    except Error as e:
        print(f'error {e}')


def create_answers_table():
    database = r'C:\Users\я\PycharmProjects\pythonProject3\quiz.sqlite'
    conn = create_connection(database)
    c = conn.cursor()
    query = """
        CREATE TABLE IF NOT EXISTS answers(
        question_id INTEGER PRIMARY KEY AUTOINCREMENT,
        wrong_answer TEXT NOT NULL,
        wrong_answer2 TEXT NOT NULL, 
        wrong_answer3 TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        theme_id INTEGER NOT NULL);"""
    try:
        c.execute(query)
        conn.commit()
        conn.close()
        print('executed')
        time.sleep(1)
    except Error as e:
        print(f'error {e}')



def password_check(data: str) -> bool:
    # '''Функция для проверки паролей на надежность:
    # не менее 10 символов, одна или более букв верхнего регистра,
    # одна или более букв нижнего регистра, одна или более цифр, латинские буквы'''
    return len(data) > 9 and all(re.search(p, data) for p in ('[A-Z]', '\d', '[a-z]'))


def check_login(username):
    database = r'C:\Users\я\PycharmProjects\pythonProject3\quiz_users.sqlite'
    conn = create_connection(database)
    c = conn.cursor()
    query = f""" 
    SELECT login from users
    WHERE login = (?);"""
    try:
        c.execute(query, username)
        print('проверка логина')
        time.sleep(1)
    except Error as e:
        print(f'error {e}')

    empty_list = c.fetchall()

    if empty_list:
        conn.close()
        return True
    else:
        conn.close()
        return False


def registration():
    database = r'C:\Users\я\PycharmProjects\pythonProject3\quiz_users.sqlite'
    conn = create_connection(database)
    c = conn.cursor()
    while True:
        login = str(input('Введите ваш логин'))
        if not check_login(login):
            break
        else:
            print("данный логин уже существует")
            time.sleep(1)
    while True:
        password = str(input('Введите пароль(не менее 10 символов, 1 цифра, одна заглавная буква, ТОЛЬКО латиница):'))
        if password_check(password):
            break
        else:
            print('пароль не соответствует требованиям')
            time.sleep(1)
    safeword = str(input('Введите слово для восстановления пароля'))
    email = str(input('Введите ваш адрес электронной почты чтобы мы засрали его нахуй всякой ебаной рассылкой'))
    reg_tuple = (login, password, safeword, email)
    reg_inject = """
    INSERT INTO
        users(login,password,safeword,email)
    VALUES
    (?,?,?,?);"""
    try:
        c.execute(reg_inject, reg_tuple)
        print('регистрация пользователя')
        time.sleep(1)
    except Error as e:
        print(f'Ошибка:{e}')
    new_member_info_query = """
        SELECT login, password FROM users
        WHERE login = (?);"""
    try:
        c.execute(new_member_info_query, (login,))
        new_member_info = c.fetchall()[0]
        print(f'Вы были зарегистрированы под логином {new_member_info[0]}. ')
        print(f'Ваш пароль: {new_member_info[1]}')
        time.sleep(1)
    except Error as e:
        print(f'Ошибка:{e}')
    conn.commit()
    conn.close()


def quiz_users_db_cont():
    database = r'C:\Users\я\PycharmProjects\pythonProject3\quiz_users.sqlite'
    conn = create_connection(database)
    c = conn.cursor()
    all_users_command = """SELECT * FROM users;"""
    try:
        c.execute(all_users_command)
    except Error as e:
        print(f'error {e}')
    all_users_info = c.fetchall()
    for user in all_users_info:
        print(user)
    else:
        time.sleep(1)
    conn.close()


def quiz_db_cont():
    database = r'C:\Users\я\PycharmProjects\pythonProject3\quiz_users.sqlite'
    conn = create_connection(database)
    c = conn.cursor()
    all_quiz_command = """SELECT * FROM answers;"""
    theme_list = ['meme_questions','math_questions'] #циклично выводит все вопросы из таблиц с вопросами
    for theme in theme_list:
        try:
            query = f"""SELECT * FROM {theme}"""
            c.execute(query)
            content = c.fetchall()
            for line in content:
                print(line)
            else:
                time.sleep(1)
        except Error as e:
            print(f'error {e}')
    try:
        c.execute(all_quiz_command)
    except Error as e:
        print(f'error {e}')
    all_questions_info = c.fetchall()
    for question in all_questions_info:
        print(question)
    else:
        time.sleep(1)
    conn.close()


def check_password(username, user_password):
    database = r'C:\Users\я\PycharmProjects\pythonProject3\quiz_users.sqlite'
    conn = create_connection(database)
    c = conn.cursor()
    query = """
    SELECT password from users
    where login = (?); """
    try:
        c.execute(query, username)
    except Error as e:
        print(f'error {e}')
    if user_password != c.fetchall()[0][0]:
        print('Неверный пароль')
        time.sleep(1)
        conn.close()
        return False
    else:
        print('вы авторизированы')
        conn.close()
        time.sleep(1)
        return True


def authorization():
    while True:
        login = str(input('Введите ваш логин'))
        if not check_login(login):
            print("данный логин не зарегистрирован")
            time.sleep(1)
        else:
            break
    while True:
        password = str(input('введите пароль:'))
        if check_password(login, password):
            break


def create_table_questions_meme():
    database = r'C:\Users\я\PycharmProjects\pythonProject3\quiz.sqlite'
    conn = create_connection(database)
    c = conn.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS meme_questions(
    theme_id INT DEFAULT 1,
    question_text TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    question_id INT NOT NULL,
    FOREIGN KEY(question_id) REFERENCES answers(question_id));
    """
    try:
        c.execute(query)
        print('executed')
        conn.commit()
    except Error as e:
        print(f'error {e}')
    conn.close()



def ask_question():
    database = r'C:\Users\я\PycharmProjects\pythonProject3\quiz.sqlite'
    conn = create_connection(database)
    c = conn.cursor()
    theme_list = ['meme_questions','math_questions']
    print('Добро пожаловать в викторину.')
    time.sleep(1)
    print('Пожалуйста, выберите тему из предложенного списка:')
    time.sleep(1)
    print('1) Кросс-тема:')
    for i in range(len(theme_list)):
        print(f'{i + 2}) {theme_list[i]}')
    while True:
        try:
            theme_choice_num = int(input())
            if (theme_choice_num -1)  > len(theme_list) or theme_choice_num <= 0:
                print('Такой темы не существует.')
                time.sleep(1)
            elif theme_choice_num == 1:
                print('Вы выбрали Кросс-тему.')
                time.sleep(1)
                for i in range(len(theme_list)):
                    print(f'{i + 1}) {theme_list[i]}')
                while True:
                    first_theme = int(input('Пожалуйста, выберите 1 тему:'))
                    time.sleep(1)
                    second_theme = int(input('Пожалуйста, выберите 2 тему:'))
                    time.sleep(1)
                    if first_theme == second_theme:
                        print('ВЫБЕРИТЕ РАЗНЫЕ ТЕМЫ')
                        time.sleep(1)
                    else:
                        break
                try:
                    c.execute(f'SELECT question_text, question_id FROM {theme_list[first_theme -1]}')
                except Error as e:
                    print(f'error {e}')
                questions_temp = c.fetchall()
                try:
                    c.execute(f'SELECT question_text, question_id FROM {theme_list[second_theme -1]}')
                except Error as e:
                    print(f'error {e}')
                second_chunk = c.fetchall()
                for elem in second_chunk:
                    questions_temp.append(elem)
                while True:
                    try:
                        limit = int(input('Введите количество вопросов:'))
                        time.sleep(1)
                        break
                    except ValueError:
                        print('Вы ввели не число!')
                        time.sleep(1)
                ask_question_part_2(questions_temp,limit)
                return
            else:
                print(f'Вы выбрали тему {theme_list[theme_choice_num -2]}')
                time.sleep(1)
                break
        except ValueError:
            print('ВЫ ВВЕЛИ НЕ ЧИСЛО')
            time.sleep(1)

    theme_choice = f"""
        SELECT question_text, question_id 
        FROM {theme_list[theme_choice_num - 1]}"""
    limit = int(input('Введите количество вопросов'))
    time.sleep(1)
    try:
        c.execute(theme_choice)
    except Error as e:
        print(f'error {e}')

    questions_temp = list(c.fetchall())
    conn.close()
    ask_question_part_2(questions_temp, limit)
    return


def ask_question_part_2(questions_list,limit):
    import random
    database = r'C:\Users\я\PycharmProjects\pythonProject3\quiz.sqlite'
    conn = create_connection(database)
    c = conn.cursor()
    random.shuffle(questions_list)
    questions = questions_list.copy()
    questions = questions[0:limit]
    correct_answers = 0
    for question in questions:
        print(question[0])
        question_id = question[1]

        answer_query = """
        SELECT correct_answer,wrong_answer,wrong_answer3,wrong_answer2
        FROM answers
        where question_id = (?);"""
        try:
            c.execute(answer_query,(question_id,))
        except Error as e:
            print(f'error {e}')
        answer = list(c.fetchall()[0])
        random.shuffle(answer)
        print('Варианты ответа:')
        time.sleep(1)
        try:
            number = 1
            for a in answer:
                print(number,end=' ')
                print(a)
                number +=1
        finally:
            print('Подумайте над ответом.')
            time.sleep(1)

        while True:
            digits_string = '1234567890'
            answer_digit = input('Ваш ответ(введите цифру от 1 до 4)')
            time.sleep(1)
            if len(answer_digit) == 1 and answer_digit in digits_string:
                answer_digit = int(answer_digit)
                if 0 < answer_digit < 5:
                    variant = answer[answer_digit - 1]
                    print(variant)
                    break
                else:
                    print('введено неверное значение:')
                    time.sleep(1)
            else:
                print('введено неверное значение')
                time.sleep(1)
        check_correct_answer = """
            SELECT correct_answer FROM answers
            WHERE correct_answer = (?);"""
        try:
            c.execute(check_correct_answer, (variant,))
        except Error as e:
            print(f'error {e}')
        if c.fetchall():
            correct_answers += 1
            print('ВЕРНЫЙ ОТВЕТ!')
            time.sleep(1)
        else:
            print('НЕВЕРНЫЙ ОТВЕТ')
            time.sleep(1)



    print(f'Ваш результат: {correct_answers} верных ответов из {limit} возможных')
    time.sleep(1)

    conn.close()
    return


def insert_some_answers_and_questions():
    database = r'C:\Users\я\PycharmProjects\pythonProject3\quiz.sqlite'
    conn = create_connection(database)
    c = conn.cursor()
    answers = """
    INSERT INTO answers(wrong_answer,wrong_answer2,wrong_answer3,correct_answer,theme_id)
    VALUES
        ('ты че дурак. блядь?','Охае, семпай','Нига','Да.',1),
        ('Закономерность Курцвила','Закон Мерфи','Правило Рейгана','Эффект Стрейзанд',1),
        ('Карты раздает не дилер.','Произошедшим в вип-зале','Неправильным расположением карт в запечатанной колоде','Все варианты верны',1),
        ('Мразь','Гнида','Урод','Ублюдок',1);"""
    questions = """
    INSERT INTO meme_questions(question_text,difficulty,question_id)
    VALUES
        ('Что обычно говорит Бородатый норд?','easy',1),
        ('Что описывает стремительное распространение информации, которую пытаются изъять из публичного доступа?','hard',2),
        ('Чем крайне недоволен главный герой ролика "Случай в казино"?','medium',3),
        ('С какого оскробления начинает свой монолог мужчина с ножом из фильма "Кровь и бетон"?','easy',4);"""
    try:
        c.execute(answers)
        c.execute(questions)
        conn.commit()
    except Error as e:
        print(f'error {e} ')
    conn.close()


def create_table_questions_math():
    database = r'C:\Users\я\PycharmProjects\pythonProject3\quiz.sqlite'
    conn = create_connection(database)
    c = conn.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS math_questions(
    theme_id INT DEFAULT 2,
    question_text TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    question_id INT NOT NULL,
    FOREIGN KEY(question_id) REFERENCES answers(question_id));
    """
    try:
        c.execute(query)
        print('executed')
        conn.commit()
    except Error as e:
        print(f'error {e}')
    conn.close()


def create_table_questions_template():
    database = r'C:\Users\я\PycharmProjects\pythonProject3\quiz.sqlite'
    conn = create_connection(database)
    c = conn.cursor()
    """name - менять на имя таблицы
    x - номер последней добавленной темы
    """

    query = """
    CREATE TABLE IF NOT EXISTS name_questions( 
    theme_id INT DEFAULT x+1,
    question_text TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    question_id INT NOT NULL,
    FOREIGN KEY(question_id) REFERENCES answers(question_id));
    """
    try:
        c.execute(query)
        print('executed')
        conn.commit()
    except Error as e:
        print(f'error {e}')
    conn.close()


def insert_any_questions_template():
    database = r'C:\Users\я\PycharmProjects\pythonProject3\quiz.sqlite'
    conn = create_connection(database)
    c = conn.cursor()
    answers = """
    INSERT INTO 
        answers(wrong_answer,wrong_answer2,wrong_answer3,correct_answer,theme_id)
    VALUES
        ('','','','',),
        ('','','','',),
        ('','','','',),
        ('','','','',);"""
    questions = """
    INSERT INTO 
        %%%_questions(question_text,difficulty,question_id)
    VALUES
    ('','',),
    ('','',),
    ('','',),
    ('','',);"""
    try:
        c.execute(answers)
        c.execute(questions)
        conn.commit()
    except Error as e:
        print(f'error {e} ')
    conn.close()


def insert_questions_math():
    database = r'C:\Users\я\PycharmProjects\pythonProject3\quiz.sqlite'
    conn = create_connection(database)
    c = conn.cursor()
    answers = """
    INSERT INTO 
        answers(wrong_answer,wrong_answer2,wrong_answer3,correct_answer,theme_id)
    VALUES
        ('Дуга','Радиус','Диаметр','Хорда',2),
        ('Эратосфен','Докинз','Хокинг','Гаусс',2),
        ('Факториал','Логарифм','Корень','Модуль',2),
        ('Гипербола','Дуга','Кривая','Кубическая парабола',2);"""
    questions = """
    INSERT INTO 
        math_questions(question_text,difficulty,question_id)
    VALUES
    ('Отрезок, соединяющий две точки окружности?','easy',5),
    (' Кто сказал: «Математика - царица наук, а арифметика — царица математики»?','medium',6),
    ('Абсолютная величина числа?','easy',7),
    ('График функции у = х3','hard',8);"""
    try:
        c.execute(answers)
        c.execute(questions)
        conn.commit()
    except Error as e:
        print(f'error {e} ')
    conn.close()


