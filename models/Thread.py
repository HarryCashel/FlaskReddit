from main import db
from utils import pretty_date

class Thread(db.Model):
    __tablename__ = "threads"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now())

    thread_owner = db.Column(db.Integer, db.ForeignKey("users.id"))
    parent_subreddit = db.Column(db.Integer, db.ForeignKey("subreddits.id"))

    comment = db.relationship("Comment", backref="thread", lazy="dynamic")

    # def __init__(self, title, content, thread_owner, parent_subreddit):
    #     self.title = title
    #     self.content = content
    #     self.thread_owner = thread_owner
    #     self.parent_subreddit = parent_subreddit

    def __repr__(self):
        return '<Thread %r>' % (self.title)

    def get_comments(self, order_by="timestamp"):
        """Function to return up to 50 comments that are children of a thread"""
        if order_by == "timestamp":
            return self.comment.filter_by(parent_thread=self.id).order_by(db.desc(Comment.date_created)).all()[:50]
        else:
            return self.comment.filter_by(parent_thread=self.id).order_by(db.desc(Comment.date_created)).all()[:50]


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now())

    parent_thread = db.Column(db.Integer, db.ForeignKey("threads.id"))
    comment_owner = db.Column(db.Integer, db.ForeignKey("users.id"))

    parent_comment = db.Column(db.Integer, db.ForeignKey("comments.id"))
    children = db.relationship("Comment", backref=db.backref('parent', remote_side=[id]), lazy="dynamic")

    # def __init__(self, content, parent_thread, comment_owner, parent_comment):
    #     self.content = content
    #     self.parent_thread = parent_thread
    #     self.comment_owner = comment_owner
    #     self.parent_comment = parent_comment

    def get_comments(self, order_by="timestamp"):
        """Function to return up to 50 comments that are children of a comment"""
        if order_by == "timestamp":
            return self.children.order_by(db.desc(Comment.date_created)).all()[:50]
        else:
            return self.children.order_by(db.desc(Comment.date_created)).all()[:50]

    def show_time(self):
        """Returns a human digestible version of the age of the comment"""
        local = pretty_date(self.date_created)
        return local
