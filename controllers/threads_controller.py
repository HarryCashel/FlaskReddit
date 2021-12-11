from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, get_current_user
from main import db
from models.Thread import Thread, Comment
from models.User import User
from models.Subreddit import Subreddit
from models.SubredditMembers import SubredditMembers
from schemas.ThreadSchema import thread_schema, threads_schema
from schemas.CommentSchema import comment_schema, comments_schema

threads = Blueprint("threads", __name__, url_prefix="/threads")


def check_is_thread_owner(_id):
    user_id = get_jwt_identity()

    search_query = Thread.query.get(_id)
    if not search_query:
        return abort(404, description="Thread not found")

    is_owner = Thread.query.filter_by(thread_owner=user_id).first().thread_owner

    if int(user_id) != is_owner:
        return abort(401, description="Invalid user")
    print(search_query)
    print(is_owner)
    return search_query


@threads.route("/", methods=["GET"])
def get_all_threads():
    threads = Thread.query.all()

    return jsonify(threads_schema.dump(threads))


@threads.route("/<int:thread_id>", methods=["GET"])
def get_thread(thread_id):
    thread = Thread.query.get(thread_id)

    if not thread:
        return abort(404, description="Thread not found")
    return jsonify(thread_schema.dump(thread))


@threads.route("/<int:subreddit_id>", methods=["POST"])
@jwt_required
def create_threads(subreddit_id):
    user_id = get_jwt_identity()
    subreddit = Subreddit.query.get(subreddit_id)
    thread_fields = thread_schema.load(request.json)
    is_member = SubredditMembers.query.filter_by(user_id=user_id, subreddit_id=subreddit_id).first()
    if not is_member:
        return abort(401, description="Must be a member of the subreddit to create a thread.")

    new_thread = Thread()
    new_thread.title = thread_fields["title"]
    new_thread.content = thread_fields["content"]
    new_thread.thread_owner = user_id
    new_thread.parent_subreddit = subreddit.id

    db.session.add(new_thread)
    db.session.commit()

    return jsonify(thread_schema.dump(new_thread))


@threads.route("/<int:thread_id>", methods=["DELETE"])
@jwt_required
def delete_thread(thread_id):

    thread = check_is_thread_owner(thread_id)

    db.session.delete(thread)
    db.session.commit()

    return jsonify(thread_schema.dump(thread))


@threads.route("/<int:thread_id>", methods=["PATCH"])
@jwt_required
def update_thread(thread_id):
    # check if current user owns thread
    thread = check_is_thread_owner(thread_id)
    # load json from request
    update_fields = thread_schema.load(request.json, partial=True)

    # query database for thread by id
    thread = Thread.query.filter_by(id=thread.id)

    # update specific thread and commit update to database
    thread.update(update_fields)
    db.session.commit()

    return jsonify(thread_schema.dump(thread))


@threads.route("/<int:thread_id>/comment", methods=["POST"])
def create_comment(thread_id):
    pass


@threads.route("/<int:thread_id>/comment/<int:comment_id>", methods=["PATCH"])
def update_comment(thread_id):
    pass


@threads.route("/<int:thread_id>/comment/<int:comment_id>", methods=["DELETE"])
def delete_comment(thread_id):
    pass


