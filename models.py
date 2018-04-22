


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
