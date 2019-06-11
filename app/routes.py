from flask import render_template, json, request, redirect, url_for, flash, request
from app.models import User, Quiz
from app.form import RegistrationForm, LoginForm
from app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import os
import json
import random
import flask
import copy

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, college=form.college_name.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfully','success')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data )
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else :
            flash(f'LogIn Unsuccessful!','danger')
    return render_template('login.html',form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

quiz_dir = 'quizes'
quizzes = {}
for quiz in os.listdir(quiz_dir):
    quizzes[quiz] = json.loads(open(os.path.join(quiz_dir, quiz)).read())

@app.route('/objective')
@login_required
def objective():
    return render_template('objective.html', quiz_names=zip(quizzes.keys(), map(lambda q: q['name'], quizzes.values())))

@app.route('/quiz/<id>')
def quiz(id):
    if id not in quizzes:
        return flask.abort(404)
    quiz = copy.deepcopy(quizzes[id])
    questions = list(enumerate(quiz["questions"]))
    random.shuffle(questions)
    quiz["questions"] = map(lambda t: t[1], questions)
    ordering = list(map(lambda t: t[0], questions))

    return render_template('quiz.html', id=id, quiz=quiz, quiz_ordering=json.dumps(ordering))


@app.route('/check_quiz/<id>', methods=['POST'])
def check_quiz(id):
    ordering = json.loads(flask.request.form['ord'])
    quiz = copy.deepcopy(quizzes[id])
    print (flask.request.form)
    quiz['questions'] = sorted(quiz['questions'], key=lambda q: ordering.index(quiz['questions'].index(q)))
    print (quiz['questions'])
    answers = dict( (int(k), quiz['questions'][int(k)]['options'][int(v)]) for k, v in flask.request.form.items() if k != 'ord' )

    print (answers)

    if not len(answers.keys()):
        return flask.redirect(flask.url_for('quiz', id=id))

    for k in range(len(ordering)):
        if k not in answers:
            answers[k] = [None, False]

    answers_list = [ answers[k] for k in sorted(answers.keys()) ]
    number_correct = len(list(filter(lambda t: t[1], answers_list)))

    return flask.render_template('check_quiz.html', quiz=quiz, question_answer=zip(quiz['questions'], answers_list), correct=number_correct, total=len(answers_list))

@app.route('/practical')
@login_required
def practical():
    return render_template('practical.html')