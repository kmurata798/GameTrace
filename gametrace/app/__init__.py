from datetime import datetime
from flask import Flask, escape, request, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from models import User, Post

app = Flask(__name__)
app.config['SECRET_KEY'] = '1e51fab5a353df7272058fda03dd063b'
# SQLAlchemy is a database!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)