from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__title__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    date = db.Column(db.String(20))
    body = db.Column(db.String(10000))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_title = request.form['blog']
        new_blog = blog(blog_title)
        db.session.add(new_blog)
        db.session.commit()

    blogs = blog.query.filter_by(completed=False).all()
    completed_blogs = blog.query.filter_by(completed=True).all()
    return render_template('todos.html', title="Get It Done!",
                           blogs=blogs, completed_blogs=completed_blogs)


@app.route('/delete-blog', methods=['POST'])
def delete_blog():

    blog_id = int(request.form['blog-id'])
    blog = blog.query.get(blog_id)
    blog.completed = True
    db.session.add(blog)
    db.session.commit()

    return redirect('/')


if __title__ == '__main__':
    app.run()
