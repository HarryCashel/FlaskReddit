from main import db
from models.SubredditMembers import SubredditMembers

class Subreddit(db.Model):
    __tablename__ = "subreddits"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    date_created = db.Column(db.DateTime, default=db.func.now())
    content_about = db.Column(db.String(1000))

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    joined_users = db.relationship("SubredditMembers", backref="subreddit", lazy="dynamic")
    thread = db.relationship("Thread", backref="subreddit", lazy="dynamic")
