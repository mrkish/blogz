from flask import Flask, request, redirect, render_template, flash, session
from datetime import datetime
from hashutils import make_salt, make_pw_hash, check_pw_hash
from passutils import verify_password
from app import app,db
from models import User, Blog
import cgi

# Requires login but allows CSS to be loaded across all pages
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'user' not in session and '/static/' not in request.path:
        return redirect('/login')

# Main content page
@app.route('/blog')
def index():
    # TODO: I want to be able to handle non-alpha blog ID requests and display the appropriate errors.
    if request.args.get('id'):
        #single_view = True
        single_blog = 0
        blog_id = request.args.get('id')

        if not blog_id.isnumeric():
            flash('Blog ID must be a integer, not an alpha character.')
            return redirect('/blog')

        if single_blog == None:
            flash('Blog id {0} does not exist!'.format(blog_id), 'error')
            return redirect('/blog')

        blog_id = int(blog_id)
        single_blog = Blog.query.get(blog_id)

        return render_template('blog.html', single_view=True, page_title=single_blog.title,blog_title=single_blog.title,blog_body=single_blog.body,blog_dateTime=single_blog.dateTime, blog_author=single_blog.author.username)

    if request.args.get('userID'):
        user_id= User.query.filter_by(username=request.args.get('userID')).first()
        blogs = Blog.query.filter_by(author=user_id).all()
        userName = request.args.get('userID')
        
        if len(blogs) == 0:
            flash('There are no registered users named {0}!'.format(userName), 'error')
            userName = 'Nobody, no one, no who'
            
        return render_template('singleUser.html', page_title=userName + "'s Posts!", author=userName, blogs=blogs, single_view=False)

    blogs = Blog.query.order_by(Blog.dateTime.desc()).all()
    
    return render_template('blog.html', page_title="Blogs!", blogs=blogs, single_view=False)

# Displays all users
@app.route('/users')
def users():
    users = User.query.all()
    return render_template('index.html', page_title="Users!", users=users)

# Page to input a new post to the blog
@app.route('/newpost', methods=['POST','GET'])
def newpost():
    username = session['user']

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
        new_blog = Blog(blog_title, blog_body, dateTime, user)
        db.session.add(new_blog)
        db.session.commit()
        new_blog_id = str(new_blog.id)

        return redirect('/blog?id=' + new_blog_id)

    return render_template('newpost.html', page_title=username + "'s New Post!")

# Page to create a user account; requires a user name and a password (double-entered to verify input)
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    user = ''
    password = ''
    verify = ''

    user_error = ''
    password_error = ''
    password_match_error = ''

    if request.method == 'POST':
        user = cgi.escape(request.form['user'])
        password = cgi.escape(request.form['password'])
        verify = cgi.escape(request.form['verify'])
        username_exists = User.query.filter_by(username=user).first()

        if username_exists:
            user_error = 'Username already exists!'

        if not password == verify or not verify:
            password_match_error = 'Passwords do not match. (Copy and paste, yo)'

        if not verify_password(password, verify):
            password_error = 'Password requirements: 8-20 length, 1 digit, 1 uppercase, and one special character.'

        if user_error or password_error or password_match_error:
            user = ''
            password = ''
            verify = ''

            return render_template('signup.html', title='Signup', user=user, password=password, verify=verify, user_error=user_error, password_error=password_error, password_match_error=password_match_error)

        new_user = User(user,password)
        db.session.add(new_user)
        db.session.commit()
        session['user'] = new_user.username

        return redirect('/blog')

    return render_template('signup.html', title='Signup', user=user, password=password, verify=verify)

# Login page for users with existing accounts
@app.route('/login', methods=['GET','POST'])
def login():
    user_error = ''
    password_error = ''

    if request.method == 'POST':
        username = cgi.escape(request.form['username'])
        password = cgi.escape(request.form['password'])
        user = User.query.filter_by(username=username).first()

        if not user:
            user_error = 'User name not found or not entered!'
            return render_template('login.html', user_error=user_error)

        if not check_pw_hash(password, user.passwordHash):
            password_error = 'Incorrect password!'
            return render_template('login.html', password_error=password_error, user_error=user_error)

        if not user_error or password_error:
            session['user'] = user.username
            return redirect('/blog')

        session['user'] = user.username
        return redirect('/blog')

    return render_template('login.html')

#
@app.route('/logout', methods=['GET'])
def logout():
    del session['user']
    return redirect('/')

#
if __name__ == '__main__':
    app.run()
