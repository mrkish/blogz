from flask import Flask, request, redirect, render_template, flash, session
from datetime import datetime
from hashutils import make_salt,make_pw_hash,check_pw_hash
from passutils import verify_email, verify_password
from app import app,db
from models import User, Blog
import cgi

# Requires login
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')

# Redirects root directory to login
#@app.route('/')
#def index():
#    return redirect('/login')

# Main content page
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

# Page to input a new post to the blog
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

        user = User.query.filter_by(username=session['user']).first()
        author_id = user.id

        new_blog = Blog(blog_title, blog_body, dateTime, author_id)
        db.session.add(new_blog)
        db.session.commit()

        new_blog_id = str(new_blog.id)

        return redirect('/blog?id=' + new_blog_id)

    return render_template('newpost.html', page_title='New Post')

# Page to create a user account; requires a user name and a password (double-entered to verify input)
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    user = ''
    password = ''
    verify = ''

    password_error = ''
    password_match_error = ''

    if request.method == 'POST':
        user = cgi.escape(request.form['user'])
        password = cgi.escape(request.form['password'])
        verify = cgi.escape(request.form['verify'])

        if not password == verify or not verify:
            password_match_error = 'Passwords do not match. (Copy and paste, yo)'

        if not verify_password(password, verify):
            password_error = 'Password requirements: 8-20 length, 1 digit, 1 uppercase, and one special character.'

        if password_error or password_match_error:
            password = ''
            verify = ''

            return render_template('signup.html', title='Signup', user=user, password=password, verify=verify, email_error=email_error, password_error=password_error, password_match_error=password_match_error)

        new_user = User(user,password)
        db.session.add(new_user)
        db.session.commit()
        session['user'] = new_user.username

        return redirect('/blog')

    return render_template('signup.html', title='Signup', user=user, password=password, verify=verify)

# Login page for users with existing accounts
@app.route('/login', methods=['GET','POST'])
def login():
    '''Provides login page for registered users to login. Verifies password hash if form data is submitted'''
 
    user_error = ''
    password_error = ''

    if request.method == 'POST':
        username = cgi.escape(request.form['username'])
        password = cgi.escape(request.form['password'])

        user = User.query.filter_by(username=username).first()

        if not user:
            user_error = 'User name not found or not entered!'

        if not check_pw_hash(password, user.passwordHash):
            password_error = 'Incorrect password!'

        if not user_error or password_error:
            session['user'] = user.username
            return redirect('/blog')

        return redirect('/login')

    return render_template('login.html')

#
@app.route('/logout')
def logout():
    del session['user']
    return redirect('/login')

#
if __name__ == '__main__':
    app.run()
