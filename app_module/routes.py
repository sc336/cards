#!/usr/bin/env python3
from app_module import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app_module.models import User, SALT
from app_module.forms import LoginForm


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('card.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print(f'current user {current_user.name}')
        return redirect(url_for('index', _anchor='greeting'))
    elif 'link_string' in request.args.to_dict():
        possible_user = db.users.find_one({'link_string':request.args.to_dict()['link_string']})
        if not possible_user is None:
            login_user(User(username=possible_user['username']))
            next_page = url_for('index', _anchor='greeting')
            return redirect(next_page)

    form = LoginForm()
    if form.validate_on_submit():
        doc_user = db['users'].find_one({'username':form.username.data})
        if doc_user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        user = User(username = doc_user['username'])
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            #The netloc != '' protects against malicious cross-site redirection
            next_page = url_for('index', _anchor='greeting')
        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Goodbye!')
    return redirect(url_for('index'))

