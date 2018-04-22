from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from hashutils import make_salt,make_pw_hash,check_pw_hash
from passutils import verify_email, verify_password
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:speakyourmind@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'hluafweafhuwalhufwi'
db = SQLAlchemy(app)


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
    username = db.Column(db.String(50))
    passwordHash = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='author')

    def __init__(self, username, password):
        self.username = username
        self.passwordHash = make_pw_hash(password)

@app.route('/blog')
def index():

    if request.args.get('id'):
        single_view = True
        blog_id = int(request.args.get('id'))

        single_blog = Blog.query.get(blog_id)
        
        if single_blog == None:
            flash('Blog id {0} does not exist!'.format(blog_id), 'error')
            return redirect('/blog')
        
        blog_title = single_blog.title
        blog_body = single_blog.body
        blog_dateTime = single_blog.dateTime
        
        return render_template('blog.html', single_view=True, page_title=blog_title,blog_title=blog_title,blog_body=blog_body,blog_dateTime=blog_dateTime)

    blogs = Blog.query.order_by(Blog.dateTime.desc()).all()
    
    return render_template('blog.html', page_title="Blogs!", blogs=blogs, single_view=False)

@app.route('/newpost', methods=['POST','GET'])
def newpost():

    if request.method == 'POST':
        blog_title = cgi.escape(request.form['title'])
        blog_body = cgi.escape(request.form['body'])

        no_title_message = ''
        no_body_message = ''

        if not blog_title:
            no_title_message = 'Missing blog title!'
            
        if not blog_body:
            no_body_message = 'Missing blog body!'

        if no_body_message or no_title_message:

            return render_template('newpost.html', page_title='New Post', no_title_message=no_title_message, no_body_message=no_body_message, blog_title=blog_title,blog_body=blog_body)
        
        dateTime = datetime.utcnow()

        new_blog = Blog(blog_title, blog_body, dateTime, owner_id)
        db.session.add(new_blog)
        db.session.commit()

        new_blog_id = str(new_blog.id)

        return redirect('/blog?id=' + new_blog_id)

    return render_template('newpost.html', page_title='New Post')

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/', methods=['POST', 'GET'])
def signup():
    user = ''
    password = ''
    verify = ''
    email = ''

    user_error = ''
    email_error = ''
    password_error = ''
    password_match_error = ''

    if request.method == 'POST':
        email = cgi.escape(request.form['email'])
        password = cgi.escape(request.form['password'])
        verify = cgi.escape(request.form['verify'])

        if len(user) < 3 and not user_error:
            user_error = 'User name too short.'

        if not password == verify or not verify:
            password_match_error = 'Passwords do not match. (Copy and paste, yo)'

        if not verify_password(password, verify):
            password_error = 'Password requirements: 8-20 length, 1 digit, 1 uppercase, and one special character.'

        if email:
            if len(email) < 3 or len(email) > 20:
                email_error = 'Emails must be between 3-20 characters. '

            if not verify_email(email):
                email_error = email_error + 'Invalid formating and/or TLD. Only .com/.edu/.org/.net addresses accepted.'

            if email_error:
                email = ''

        if email_error or password_error or password_match_error:
            password = ''
            verify = ''

            return render_template('signup.html', title='Signup', email=email, password=password, verify=verify, email_error=email_error, password_error=password_error, password_match_error=password_match_error)

        new_user = User(email,password)
        db.session.add(new_user)
        db.session.commit()
        session['user'] = new_user.username

        return redirect('/blog')

    return render_template('signup.html', title='Signup', user=user, password=password, verify=verify, email=email)

@app.route('/login', methods=['GET','POST'])
def login():
    '''Provides login page for registered users to login. Verifies password hash if form data is submitted'''
    
    username = user.username
    user = User.query.filter_by(sessionUser=session['username']).first()

    if request.method == 'POST':
        user = cgi.escape(request.form['username'])
        password = cgi.escape(request.form['password'])

        if username and check_pw_hash(password, user.pw_hash):
            return redirect('/blog')
        else:
            return redirect('/login')

    return render_template('/login')


if __name__ == '__main__':
    app.run()
