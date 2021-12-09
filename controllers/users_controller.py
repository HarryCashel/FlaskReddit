from flask import Blueprint, request, jsonify, abort
from schemas.UserSchema import user_schema, users_schema
from models.User import User
from main import db, bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

users = Blueprint("users", __name__, url_prefix="/users")


@users.route("/all", methods=["GET"])
def get_all_users_index():
    # Return all users
    users = User.query.all()

    return jsonify(users_schema.dump(users))


@users.route("/register", methods=["POST"])
def auth_register():
    user_fields = user_schema.load(request.json)

    user = User.query.filter_by(email=user_fields["email"]).first()

    if user:
        return abort(401, description="Email already registered")

    user = User()
    user.email = user_fields["email"]
    user.set_password(user_fields["password"])
    user.username = user_fields["username"]

    db.session.add(user)
    db.session.commit()

    return jsonify(user_schema.dump(user))


@users.route("/login", methods=["POST"])
def user_login():
    user_fields = user_schema.load(request.json)

    user = User.query.filter_by(email=user_fields["email"]).first()
    user_fields["username"] = user.username
    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="No user with those credentials")

    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)

    return jsonify({"token": access_token})


@users.route("/", methods=["GET"])
@jwt_required
def get_user():
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        abort(401, description="Invalid user")

    return jsonify(user_schema.dump(user))


@users.route("/", methods=["PATCH"])
@jwt_required
def update_user():
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id)

    if not user:
        abort(401, description="Invalid user")

    update_fields = user_schema.load(request.json, partial=True)
    user.update(update_fields)
    db.session.commit()

    return jsonify(user_schema.dump(user[0]))


@users.route("/", methods=["DELETE"])
@jwt_required
def delete_user():
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        abort(401, description="Invalid user")
    db.session.delete(user)
    db.session.commit()

    return jsonify(user_schema.dump(user))
