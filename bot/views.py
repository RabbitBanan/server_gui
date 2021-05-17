from bot import app, mysql
import os
from bot.forms import LoginForm
from flask import render_template, flash, redirect, request, url_for, session, make_response

import json
import hashlib

conn = mysql.connect()
cursor = conn.cursor()



def show_bot_config():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "BOT_CONFIG.json")
    data = json.load(open(json_url, encoding='utf8'))
    return data


@app.route('/index')
@app.route('/')
def index():
    cursor.execute("SELECT id, name, iswork FROM bot_bots WHERE isdelete = 0")
    data = cursor.fetchall()
    return render_template("index.html",
                           title='Конфигуратор чат-бота',
                           count=len(data),
                           data=data)



@app.route('/bot', methods = ['GET', 'POST'])
def bot():
    if request.method == 'POST':
        session['edit_type'] = request.form['edit_type']
        print(session)
        print(url_for('edit'))
        return redirect(url_for('edit'))

    templates = show_bot_config()
    type_nlp_module = templates['type_nlp_module']
    intents = templates['data_set']['intents']
    hello_phrases = templates['data_set']['hello_phrases']
    failure_phrases = templates['data_set']['hello_phrases']
    return render_template("index.html",
                           title='Конфигуратор чат-бота',
                           templates=templates)



@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request.cookies)
    print(request.form)
    if request.method == 'POST':
        _name = request.form['name']
        _password = hashlib.md5('{0}'.format(request.form['password']).encode('utf-8')).hexdigest()
        if _name and _password:
            cursor.execute('SELECT COUNT(*) FROM bot_users WHERE login = "{0}" and passwrd ="{1}"'.format(_name, _password))
            data = cursor.fetchall()
            if (data[0][0]) == 1:
                res = make_response("Setting a cookie")
                res.set_cookie('user', _name)
                flash('Пользователь авторизован')
            else:
                flash('Ошибка авторизации: не верный логин и пароль')
            conn.commit()


    log =''
    if request.cookies.get('user'):
        log = request.cookies.get('user')

    return render_template("login.html", title='Конфигуратор чат-бота', user=log)



@app.route('/edit')
def edit():

    return render_template('edit.html')