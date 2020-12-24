#!/usr/bin/env python3
from flask import Flask
from flask_login import LoginManager
import pymongo
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Make this actually secure sometime in the future'
app.config['MONGODB_URI'] = 'mongodb://localhost:27017/'

db = pymongo.MongoClient(app.config['MONGODB_URI'])['cardsdb']

login = LoginManager(app)
login.login_view = 'login'

from app_module import routes, models
