import werkzeug.security

from models.User import User, UserMixin
from models.Subreddit import Subreddit
from models.Thread import Thread
from models.SubredditMembers import SubredditMembers
from forms import LoginForm, RegisterForm, CreateSubreddit, CreateThread, JoinSub
from main import db, login_manager, bootstrap
from schemas.UserSchema import user_schema
from flask import Blueprint, render_template, flash, redirect, url_for, abort, request
from flask_login import current_user, login_user, logout_user, login_required
from controllers.web_users_controllers import load_user, unauthorised, get_user_subreddits, get_subreddits, get_threads

web_reddits = Blueprint("web_reddits", __name__, url_prefix="/r")


def get_sub_threads(subreddit_name):
    """Queries database for all threads that are children to the parameter subreddit_name.
    Returns a list of threads"""

    subreddit = Subreddit.query.filter_by(name=subreddit_name).first().id
    threads = Thread.query.filter_by(parent_subreddit=subreddit).all()

    return threads


@web_reddits.route("/", methods=["GET"])
@login_required
def show_reddits():
    """Shows all reddits user is a member of"""
    login_form = LoginForm()
    register_form = RegisterForm()

    if not load_user(current_user.get_id()):
        return abort(401, description="Unauthorised to view this page")

    user_id = current_user.get_id()
    reddits = get_user_subreddits()

    return render_template("subreddit.html", reddits=reddits, login_form=login_form, register_form=register_form)


@web_reddits.route("/<name>")
def show_reddit(name):
    """Shows the page for a specific subreddit"""
    login_form = LoginForm()
    register_form = RegisterForm()
    user_id = current_user.get_id()
    subreddits = get_subreddits()
    join_subreddit = JoinSub()

    current_subreddit = Subreddit.query.filter_by(name=name).first()
    if not current_subreddit:
        abort(404)
    threads = get_sub_threads(name)

    return render_template(
        "view_subreddit.html", login_form=login_form, register_form=register_form, subreddits=subreddits,
        join_subreddit=join_subreddit, threads=threads, current_subreddit=current_subreddit
    )

