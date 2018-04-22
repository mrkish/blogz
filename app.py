from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:speakyourmind@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'hluafweafhuwalhufwi'

db = SQLAlchemy(app)
