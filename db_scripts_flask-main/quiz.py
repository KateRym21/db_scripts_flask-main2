# Тут буде код веб-програми
# from random import randint
from flask import Flask, session, redirect, url_for,request
from db_scripts import get_question_after, get_quizes

def start_quiz(quiz_id):
    session['quiz'] = quiz_id
    session['last_question'] = 0

def end_quiz():
    session.clear()

def quiz_form():
    """
    Формує HTML-форму для вибору вікторини з випадаючим списком.
    """
    # Початок HTML-формуляра
    html_beg = """
    <html>
        <body>
            <h2>Виберіть вікторину:</h2>
            <form method="post" action="index">
                <select name="quiz">
    """

    # Завершення HTML-формуляра
    frm_submit = """
                </select>
                <p><input type="submit" value="Вибрати"></p>
            </form>
        </body>
    </html>
    """
    # Формування опцій для випадаючого списку
    options = ""
    q_list = get_quizes()  # Отримання списку вікторин з бази
    for quiz_id, quiz_name in q_list:
        options += f'<option value="{quiz_id}">{quiz_name}</option>\n'

    # Повернення повного HTML
    return html_beg + options + frm_submit

def index():
    ''' Перша сторінка: якщо прийшли запитом GET, то вибрати вікторину,
     якщо POST - то запам'ятати id вікторини та відправляти на запитання
'''
    if request.method == 'GET':
        # вікторина не обрана, скидаємо id вікторини та показуємо форму вибору
        start_quiz(-1)
        return quiz_form()
    else:
        # отримали додаткові дані у запиті! Використовуємо їх:
        quest_id = request.form.get('quiz') # вибраний номер вікторини
        start_quiz(quest_id)
return redirect(url_for('test'))


def test():
     result = get_question_after(session['last_qestion'], session['quiz'])
     if result is None or len(result) ==0:
         return redirect(url_for('result'))
     else:
         session['last_question'] = result[0]
         return '<h1>' + str(session['quiz']) + '<br>' + str(result) + '</h1>'

def result():
     return "that's all folks!"



app = Flask(__name__)
app.add_url_rule('/', 'index', index)
app.add_url_rule('/test', 'test', test)
app.add_url_rule('/result', 'result', result)
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'

if __name__ == '__main__':
   # Запускаємо веб-сервер:
   app.run()
