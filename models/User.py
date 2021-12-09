from main import db, bcrypt
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

    joined_subreddits = db.relationship("SubredditMembers", backref="user", lazy="dynamic", cascade="all, delete")
    thread = db.relationship("Thread", backref="user", lazy="dynamic")
    comment = db.relationship("Comment", backref="user", lazy="dynamic")
    subreddit = db.relationship("Subreddit", backref="user", lazy="dynamic")

    def __repr__(self):
        """represent our object in a better format"""
        return f"<User {self.id}:{self.email}:{self.username}>"

    def set_password(self, password):
        """Create hashed password"""
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

