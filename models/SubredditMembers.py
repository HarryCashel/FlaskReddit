from main import db


class SubredditMembers(db.Model):
    __tablename__ = "subreddit_members"

    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), primary_key=True
    )
    subreddit_id = db.Column(
        db.Integer, db.ForeignKey("subreddits.id"), primary_key=True
    )

