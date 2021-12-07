from main import db
from models.Thread import Thread
from models.Subreddit import Subreddit


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(1000))
    date_created = db.Column(db.DateTime, default=db.func.now())
    role = db.Column(db.SmallInteger, default=0)

    joined_subreddits = db.relationship("SubredditMembers", backref="user", lazy="dynamic")
    thread = db.relationship("Thread", backref="user", lazy="dynamic")
    comment = db.relationship("Comment", backref="user", lazy="dynamic")
    subreddit = db.relationship("Subreddit", backref="user", lazy="dynamic")
