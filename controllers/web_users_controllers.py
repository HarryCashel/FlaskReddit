import werkzeug.security

from models.User import User
from models.Subreddit import Subreddit
from models.Thread import Thread
from models.SubredditMembers import SubredditMembers
from forms import LoginForm, RegisterForm
from main import db, login_manager, bootstrap
from schemas.UserSchema import user_schema
from flask import Blueprint, render_template, flash, redirect, url_for, abort, request
from flask_login import current_user, login_user, logout_user, login_required

web_users = Blueprint("web_users", __name__, url_prefix="/web")


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorised():
    flash("You must be logged in to view this page")
    return redirect(url_for('web_users.web_users_login'))


def get_subreddits():
    """Returns a list of subreddits to present on the home page (and in the future on sidebars etc)"""
    subreddits = Subreddit.query.filter(Subreddit.id != 1)[:5]
    return subreddits


def get_threads():
    """Returns a list of threads to present on the home page"""
    threads = Thread.query.filter(Thread.id != 1)[:25]
    return threads


@web_users.route("/", methods=["GET", "POST"])
def home():
    subreddits = (get_subreddits())
    threads = get_threads()
    login_form = LoginForm()
    signup_form = RegisterForm()

    if request.method == "POST" and login_form.validate_on_submit():
        new_user = User()
        new_user.email = login_form.email.data
        new_user.password = werkzeug.security.generate_password_hash(login_form.password.data)

        db.session.add(new_user)
        db.session.commit()

    if request.method == "POST" and signup_form.validate_on_submit():
        pass

    return render_template(
        "index.html", subreddits=subreddits, threads=threads, login_form=login_form, signup_form=signup_form
    )
