from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'hluafweafhuwalhufwi'
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))
    dateTime = db.Column(db.DateTime)

    def __init__(self, title, body, dateTime):
        self.title = title
        self.body = body
        self.dateTime = dateTime


@app.route('/blog')
def index():

    if request.method == 'GET' and request.args.get('id'):
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

        new_blog = Blog(blog_title, blog_body, dateTime)
        db.session.add(new_blog)
        db.session.commit()

        new_blog_id = str(new_blog.id)

        return redirect('/blog?id=' + new_blog_id)

    return render_template('newpost.html', page_title='New Post')


#@app.route('/delete-blog', methods=['POST'])
#def delete_blog():
#
#    blog_id = int(request.form['blog-id'])
#    blog = blog.query.get(blog_id)
#    return redirect('/')
#    blog.completed = True
#    db.session.add(blog)
#    db.session.commit()


if __name__ == '__main__':
    app.run()
