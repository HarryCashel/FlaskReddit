import werkzeug.security
from sqlalchemy import and_
from models.User import User, UserMixin
from models.Subreddit import Subreddit
from models.Thread import Thread, Comment
from models.SubredditMembers import SubredditMembers
from forms import LoginForm, RegisterForm, CreateSubreddit, CreateThread, CreateSpecificThread, JoinSub, LeaveSub, \
    CreateComment
from main import db, login_manager, bootstrap
from schemas.UserSchema import user_schema
from flask import Blueprint, render_template, flash, redirect, url_for, abort, request
from flask_login import current_user, login_user, logout_user, login_required
from controllers.web_users_controllers import load_user, unauthorised, get_user_subreddits, get_subreddits, get_threads
from controllers.web_subreddits_controller import is_member, unauthorised

web_threads = Blueprint("web_threads", __name__, url_prefix="/r")


# def get_comments(thread_id):
#     """Queries database for children comments.
#     Returns top comment."""
#     # thread = Thread.query.filter_by(id=thread_id).first()
#     comment = Comment.query.filter_by(parent_thread=thread_id)
#     return comment

def get_comment_owner(comment_id):
    """Function to query database for username of a comment owner"""
    user = Comment.query.filter_by(id=comment_id).first().comment_owner
    username = User.query.filter_by(id=user).first().username
    return username


@web_threads.route('/<int:thread_id>', defaults={'sub_name': None})
def show_thread(thread_id, sub_name):
    """Show a specific thread"""

    # objects to pass through to the template
    login_form = LoginForm()
    register_form = RegisterForm()
    comment_form = CreateComment()
    user_id = current_user.get_id()
    subreddits = get_subreddits()
    join = JoinSub()
    leave = LeaveSub()
    users = User.query.all()

    thread = Thread.query.filter_by(id=thread_id).first()

    # query for the subreddit name to pass through to the template
    if sub_name is None:
        parent_id = thread.parent_subreddit
        sub_name = Subreddit.query.filter_by(id=parent_id).first().name

    # if reddit does not exist
    current_subreddit = Subreddit.query.filter_by(name=sub_name).first()
    if not current_subreddit:
        abort(404)

    return render_template("view_thread.html", thread=thread, login_form=login_form, register_form=register_form,
                           subreddits=subreddits, join=join, leave=leave, current_subreddit=current_subreddit,
                           comment_form=comment_form, owner=get_comment_owner)


@web_threads.route("<int:thread_id>/create", methods=["POST"])
@login_required
def create_comment(thread_id):
    user_id = current_user.get_id()
    comment_form = CreateComment()

    if comment_form.submit.data:
        comment = Comment()
        comment.comment_owner = user_id
        comment.parent_thread = thread_id
        comment.content = comment_form.content.data

        db.session.add(comment)
        db.session.commit()

        return redirect(url_for("web_threads.show_thread", thread_id=thread_id))


@web_threads.route("<int:thread_id>/<int:comment>/create", methods=["POST"])
@login_required
def create_child_comment(thread_id, comment_id=None):
    user_id = current_user.get_id()
    comment_form = CreateComment()

    if comment_id == None:
        pass

    if comment_form.submit.data:
        comment = Comment()
        comment.comment_owner = user_id
        comment.parent_thread = thread_id
        comment.parent_comment = comment_id
        comment.content = comment_form.content.data

        db.session.add(comment)
        db.session.commit()

        return redirect(url_for("web_threads.show_thread", thread_id=thread_id))

