from models.User import User
from models.Subreddit import Subreddit
from models.SubredditMembers import SubredditMembers
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
    subreddits = Subreddit.query.filter(Subreddit.id != 1)[:25]
    return subreddits


@web_users.route("/")
def home():
    top_subreddits = get_subreddits()
    user = load_user(current_user.get_id())

    return render_template("index.html", subreddits=top_subreddits)