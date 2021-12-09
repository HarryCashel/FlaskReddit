from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import db
from models.User import User
from models.Subreddit import Subreddit
from models.Thread import Thread, Comment
from models.SubredditMembers import SubredditMembers
from schemas.UserSchema import user_schema, users_schema
from schemas.CommentSchema import comment_schema, comments_schema
from schemas.ThreadSchema import thread_schema, threads_schema
from schemas.SubredditSchema import subreddit_schema, subreddits_schema

subreddits = Blueprint("subreddits", __name__, url_prefix="/subreddits")


def get_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        abort(401, description="Invalid user")

    return user


def get_subreddit_id(name):
    subreddit = Subreddit.query.filter_by(name=name).first()
    return subreddit.id


def check_for_subreddit(sub_id):
    subreddit = Subreddit.query.get(sub_id)

    if not subreddit:
        abort(404, description="Subreddit does not exist")

    return subreddit


def check_member_subreddit(sub_id):
    user = get_user()
    subreddit_member = SubredditMembers.query.filter_by(
        user_id=user.id, subreddit_id=sub_id).first()

    if not subreddit_member:
        abort(401, description="Do not have permission")

    return subreddit_member


def is_owner(sub_id):
    subreddit_id = Subreddit.query.get(sub_id)

    if subreddit_id == get_user():
        return True
    return False


@subreddits.route("/", methods=["GET"])
def get_all_subreddits():
    # return all subreddits
    subreddits = Subreddit.query.all()

    return jsonify(subreddits_schema.dump(subreddits))


@subreddits.route("/", methods=["POST"])
@jwt_required
def create_subreddit():
    user = get_user()

    subreddit_fields = subreddit_schema.load(request.json)

    subreddit = Subreddit.query.filter_by(name=subreddit_fields["name"]).first()

    if subreddit:
        return abort(401, description="Subreddit with that name already exists")

    subreddit = Subreddit()
    subreddit.name = subreddit_fields["name"]
    subreddit.description = subreddit_fields["description"]
    subreddit.owner_id = user.id

    db.session.add(subreddit)
    db.session.commit()

    subreddit_members = SubredditMembers()
    subreddit_members.user_id = user.id
    subreddit_members.subreddit_id = get_subreddit_id(subreddit_fields["name"])

    db.session.add(subreddit_members)
    db.session.commit()

    return jsonify(subreddit_schema.dump(subreddit))


@subreddits.route("/<int:id>", methods=["PATCH"])
@jwt_required
def update_subreddits(id):
    check_for_subreddit(id)

    user_id = get_jwt_identity()

    check_owner = Subreddit.query.filter_by(id=id, owner_id=user_id)

    if not check_owner:
        abort(401, description="you don't own")

    subreddit = Subreddit.query.filter_by(id=id)
    update_fields = subreddit_schema.load(request.json, partial=True)
    subreddit.update(update_fields)
    db.session.commit()

    return jsonify(subreddit_schema.dump(subreddit[0]))


@subreddits.route("/<int:id>", methods=["DELETE"])
@jwt_required
def delete_subreddits(id):
    check_for_subreddit(id)

    user_id = get_jwt_identity()
    check_owner = Subreddit.query.filter_by(id=id, owner_id=user_id)

    if not check_owner:
        abort(401, description="you don't own")

    subreddit = Subreddit.query.get(id)

    db.session.delete(subreddit)
    db.session.commit()

    return jsonify(subreddit_schema(subreddit))

@subreddits.route("/<int:id>", methods=["GET"])
def get_specific_subreddits(id):
    subreddit = Subreddit.query.get(id)

    if not subreddit:
        abort(404, description="Subreddit does not exist")
    return jsonify(subreddit_schema.dump(subreddit))


@subreddits.route("/<int:id>", methods=["GET"])
def get_user_subreddits():
    pass


@subreddits.route("/join", methods=["POST"])
@jwt_required
def join_subreddit():
    pass
