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
    from faker import Faker
    faker = Faker()

    for i in range(20):
        user = User()
        user.email = f"user{i}@testing.com"
        user.username = f"name{i}"
        user.password = "123445678"
        db.session.add(user)

    db.session.commit()
    print("Tables seeded")
