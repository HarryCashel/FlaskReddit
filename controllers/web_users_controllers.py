import werkzeug.security

from models.User import User, UserMixin
from models.Subreddit import Subreddit
from models.Thread import Thread
from models.SubredditMembers import SubredditMembers
from forms import LoginForm, RegisterForm, CreateSubreddit, CreateThread
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
    return redirect(url_for('web_users.home'))


def get_subreddits():
    """Returns a list of subreddits to present on the home page (and in the future on sidebars etc)"""
    subreddits = Subreddit.query.filter(Subreddit.id != 1)[:5]
    return subreddits


def get_threads():
    """Returns a list of threads to present on the home page"""
    threads = Thread.query.filter(Thread.id != 1)[:25]
    return threads


def get_user_subreddits():
    """Returns list of subreddits user has joined"""
    if current_user.is_authenticated:

        user_id = current_user.get_id()
        member_of = SubredditMembers.query.filter_by(user_id=user_id).all()
        reddits = [Subreddit.query.filter_by(id=reddit_id) for reddit_id in member_of]
        return reddits


@web_users.route("/", methods=["GET", "POST"])
def home():
    subreddits = get_subreddits()
    threads = get_threads()
    login_form = LoginForm()
    register_form = RegisterForm()
    subreddit_form = CreateSubreddit()
    thread_form = CreateThread()

    user_id = current_user.get_id()
    member_of = SubredditMembers.query.filter_by(user_id=user_id).all()
    if member_of:
        reddits = [Subreddit.query.filter_by(id=entry.subreddit_id).first() for entry in member_of]

    else:
        reddits = None

    # check if login form is valid and submitted
    if request.method == "POST" and login_form.validate_on_submit():
        email = login_form.email.data

        # check email exists in db
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(login_form.password.data):
            login_user(user)
            flash("Success")
            return redirect(url_for("web_users.home"))
        else:
            flash("Invalid credentials.")

    if request.method == "POST" and register_form.validate_on_submit():
        email = register_form.email.data

        user = User.query.filter_by(email=email).first()

        if not user:
            new_user = User()
            new_user.email = register_form.email.data
            new_user.set_password(register_form.password.data)
            new_user.username = register_form.username.data

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            flash("Success")
            return redirect(url_for("web_users.home"))

    if user_id and reddits:

        thread_form.parent_subreddit.choices = [(g.id, g.name) for g in reddits]
        if request.method == "POST" and thread_form.validate_on_submit():
            choice = thread_form.parent_subreddit.data
            title = thread_form.title.data
            content = thread_form.content.data

            new_post = Thread()
            new_post.parent_subreddit = choice
            new_post.title = title
            new_post.content = content
            new_post.thread_owner = user_id

            db.session.add(new_post)
            db.session.commit()

            return redirect("/web")

    if user_id and subreddit_form.validate_on_submit():
        title = subreddit_form.title.data
        about = subreddit_form.about.data

        new_subreddit = Subreddit()
        new_subreddit.owner_id = user_id
        new_subreddit.name = title
        new_subreddit.description = about
        db.session.add(new_subreddit)
        db.session.commit()

        new_member = SubredditMembers()
        new_member.user_id = user_id
        new_member.subreddit_id = new_subreddit.id
        db.session.add(new_member)
        db.session.commit()

        return redirect("/web")



    return render_template("index.html", subreddits=subreddits, threads=threads,
                           current_user=current_user, login_form=login_form, register_form=register_form,
                           subreddit_form=subreddit_form, thread_form=thread_form, reddits=reddits)


@web_users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Invalid credentials. Please try again")
        if user:
            if user.check_password(password=password):
                login_user(user)
                flash("Successfully logged in")
                return redirect(url_for('web_users.home'))
    return render_template("login.html", form=form)


@web_users.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()

    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()

        if not user:
            new_user = User()
            new_user.email = form.email.data
            new_user.username = form.username.data
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            return redirect(url_for('web_users.home'))

        flash("Email in use. Please sign in")
        return redirect(url_for('login'))

    return render_template("signup.html", form=form)


# @web_users.route("/")


@web_users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("web_users.home"))
