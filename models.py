from app import db
from datetime import datetime
from hashutils import make_password_hash, check_password_hash



class Blogpost(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, content, owner, timestamp=None):
        self.title = title
        self.content = content
        self.owner = owner
        if timestamp is None:
            timestamp = datetime.utcnow()
        self.timestamp = timestamp


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(120))
    posts = db.relationship('Blogpost', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password_hash = make_password_hash(password)


