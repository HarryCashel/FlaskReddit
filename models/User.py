from main import db
from flask_login import UserMixin
from models.Thread import Thread
from models.Subreddit import Subreddit


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now())
    role = db.Column(db.SmallInteger, default=0)

    joined_subreddits = db.relationship("SubredditMembers", backref="user", lazy="dynamic")
    thread = db.relationship("Thread", backref="user", lazy="dynamic")
    comment = db.relationship("Comment", backref="user", lazy="dynamic")
    subreddit = db.relationship("Subreddit", backref="user", lazy="dynamic")

    def __repr__(self):
        """represent our object in a better format"""
        return f"<User {self.id}:{self.email}:{self.username}>"
