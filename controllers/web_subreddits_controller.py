import werkzeug.security
from sqlalchemy import and_
from models.User import User, UserMixin
from models.Subreddit import Subreddit
from models.Thread import Thread
from models.SubredditMembers import SubredditMembers
from forms import LoginForm, RegisterForm, CreateSubreddit, CreateThread, JoinSub, LeaveSub
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


def is_member(subreddit_name, user_id):
    subreddit = Subreddit.query.filter_by(name=subreddit_name).first().id
    member = SubredditMembers.query.filter_by(user_id=user_id, subreddit_id=subreddit).first()
    print(member)
    if member:
        return True
    return False


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


@web_reddits.route("/<name>", methods=["GET", "POST"])
def show_reddit(name):
    """Shows the page for a specific subreddit"""
    login_form = LoginForm()
    register_form = RegisterForm()
    user_id = current_user.get_id()
    subreddits = get_subreddits()
    join = JoinSub()
    leave = LeaveSub()
    member = is_member(name, user_id)

    current_subreddit = Subreddit.query.filter_by(name=name).first()
    if not current_subreddit:
        abort(404)
    threads = get_sub_threads(name)

    return render_template(
        "view_subreddit.html", login_form=login_form, register_form=register_form, subreddits=subreddits,
        join=join, leave=leave, threads=threads, current_subreddit=current_subreddit, member=member
    )


@web_reddits.route("/<name>/join", methods=["POST"])
@login_required
def join_subreddit(name):
    user_id = current_user.get_id()
    form = JoinSub()

    if form.submit.data:
        members = SubredditMembers()
        members.subreddit_id = Subreddit.query.filter_by(name=name).first().id
        members.user_id = user_id
        db.session.add(members)
        db.session.commit()

    return redirect(url_for("web_reddits.show_reddit", name=name))


@web_reddits.route("/<name>/leave", methods=["POST"])
@login_required
def leave_subreddit(name):
    user_id = current_user.get_id()
    form = LeaveSub()

    if form.submit.data:
        subreddit_id = Subreddit.query.filter_by(name=name).first().id
        subreddit_member = SubredditMembers.query.filter_by(user_id=user_id, subreddit_id=subreddit_id).first()
        print("removed member")
        if not subreddit_member:
            print("didn't work")
            return redirect(url_for("web_reddits.show_reddit", name=name))
        db.session.delete(subreddit_member)
        db.session.commit()

        return redirect(url_for("web_reddits.show_reddit", name=name))