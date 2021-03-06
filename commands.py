from main import db
from flask import Blueprint

db_commands = Blueprint("db-custom", __name__)


@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created!")


@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted")


@db_commands.cli.command("seed")
def seed_db():
    from models.User import User
    from models.Subreddit import Subreddit
    from models.SubredditMembers import SubredditMembers
    from models.Thread import Thread
    from faker import Faker
    from main import bcrypt
    import random

    faker = Faker()
    users = []
    subreddits = []
    member = []

    for i in range(5):
        user = User()
        user.email = f"user{i}@testing.com"
        user.username = faker.name()
        user.password = bcrypt.generate_password_hash("12345678").decode("utf-8")
        db.session.add(user)
        users.append(user)

    db.session.commit()

    for i in range(10):
        subreddit = Subreddit()
        subreddit.name = faker.catch_phrase()
        subreddit.description = "description"
        subreddit.owner_id = random.choice(users).id
        db.session.add(subreddit)
        subreddits.append(subreddit)
        db.session.commit()

        subreddit_member = SubredditMembers()
        subreddit_member.subreddit_id = subreddit.id
        subreddit_member.user_id = subreddit.owner_id
        db.session.add(subreddit_member)

    db.session.commit()

    for i in range(30):
        owner = random.choice(users).id
        sub_id = Subreddit.query.filter_by(owner_id=owner).first()
        if sub_id:
            thread = Thread()
            thread.title = faker.catch_phrase()
            thread.content = faker.paragraph(nb_sentences=2)
            thread.thread_owner = owner
            thread.parent_subreddit = sub_id.id

            db.session.add(thread)

    db.session.commit()

    print("Tables seeded")
