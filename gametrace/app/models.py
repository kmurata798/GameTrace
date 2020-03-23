from datetime import datetime
from __main__ import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    image_file = db.Column(db.String(25), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # Referencing the Post Class
    posts = db.relationship('Post', backref='author', lazy=True)
    # In posts field, 'backref' is similar to adding another column to the Post model.
    # This is how we do ONE TO MANY for users and posts. We can find who made a post by using 'author'

    def __repr__(self):
        return f"User('{self.username}', '{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # Referencing the table name/column name
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"