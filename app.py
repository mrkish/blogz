from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
#from datetime import datetime
#from hashutils import make_salt, make_pw_hash, check_pw_hash
#from passutils import verify_email, verify_password
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:speakyourmind@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'hluafweafhuwalhufwi'

db = SQLAlchemy(app)
