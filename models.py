from app import db
from hashutils import make_pw_hash

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))
    dateTime = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, dateTime, author):
        self.title = title
        self.body = body
        self.dateTime = dateTime
        self.author = author


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    passwordHash = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='author')

    def __init__(self, username, password):
        self.username = username
        self.passwordHash = make_pw_hash(password)
