from main import db


class Thread(db.Model):
    __tablename__ = "threads"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now())

    thread_owner = db.Column(db.Integer, db.ForeignKey("users.id"))
    parent_subreddit = db.Column(db.Integer, db.ForeignKey("subreddits.id"))

    comment = db.relationship("Comment", backref="thread", lazy="dynamic")


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now())

    parent_thread = db.Column(db.Integer, db.ForeignKey("threads.id"))
    comment_owner = db.Column(db.Integer, db.ForeignKey("users.id"))

    parent_comment = db.Column(db.Integer, db.ForeignKey("comments.id"))
    children = db.relationship("Comment", backref=db.backref('parent', remote_side=[id]), lazy="dynamic")
