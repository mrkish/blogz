from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, dateTime):
        self.title = title
        self.body = body
        self.dateTime = dateTime
        self.owner_id = owner_id

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))
    blogs = db.Column(db.Integer, db.ForeignKey('blog.id'))

    def __init__(self, title, body, dateTime):
        self.username = username
        self.password = password

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

@app.before_request()
def before_request():
    if (not user.id) and (current_url is not '/login' or '/signup')
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
        user = cgi.escape(request.form['user'])
        password = cgi.escape(request.form['password'])
        verify = cgi.escape(request.form['verify'])
        email = cgi.escape(request.form['email'])

        if not user:
            user_error = ' Please enter a user name to proceed.'

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

        if user_error or email_error or password_error or password_match_error:
            password = ''
            verify = ''

            return render_template('signup.html', title='Signup', user=user, useremail=email, password=password, verify=verify, user_error=user_error, email_error=email_error, password_error=password_error, password_match_error=password_match_error)

        return render_template('welcome.html', title='Welcome, ' + user + '!', user=user)

    return render_template('signup.html', title='Signup', user=user, password=password, verify=verify, email=email)

def verify_email(email):
    '''Checks for valid email via regex; returns a bool.
    Only admits common TLD emails.'''

    valid_email = re.compile('\w.+@\w+.(net|edu|com|org)')

    if valid_email.match(email):
        return True
    else:
        return False

def verify_password(password, verify):
    '''Checks for password symmetry and min. requirements via regex; returns a bool.
    Requirements: 8-20 length, 1 special, 1 uppercase, 1 digit'''

    valid_pass = re.compile(
        '(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#@$!%*?&])[A-Za-z\d@$#!%*?&]{8,20}')

    if password == verify and valid_pass.match(password):
        return True
    else:
        return False

if __name__ == '__main__':
    app.run()
