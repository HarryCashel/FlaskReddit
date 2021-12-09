from flask import Blueprint, request, jsonify, abort
from schemas.UserSchema import user_schema, users_schema
from models.User import User
from main import db, bcrypt


users = Blueprint("users", __name__, url_prefix="/users")


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


@users.route("/", methods=["GET"])
def user_index():
    # Return all users
    users = User.query.all()

    return jsonify(users_schema.dump(users))


@users.route("/login", methods=["POST"])
def user_login():
    user_fields = user_schema.load(request.json)

    user = User.query.filter_by(email=user_fields["email"]).first()
    user_fields["username"] = user.username
    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="No user with those credentials")

    return "token"

# @users.route("/<int:id>", methods=["GET"])
# def user_show(id):
#     # Return a single user
#     sql = "SELECT * FROM users WHERE id = %s;"
#     cursor.execute(sql, (id,))
#     user = cursor.fetchone()
#     return jsonify(user)
#
#
# @users.route("/<int:id>", methods=["PUT", "PATCH"])
# def user_update(id):
#     # Update a user
#     sql = "UPDATE users SET title = %s WHERE id = %s;"
#     cursor.execute(sql, (request.json["title"], id))
#     connection.commit()
#
#     sql = "SELECT * FROM users WHERE id = %s"
#     cursor.execute(sql, (id,))
#     user = cursor.fetchone()
#     return jsonify(user)
#
#
# @users.route("/<int:id>", methods=["DELETE"])
# def user_delete(id):
#     sql = "SELECT * FROM users WHERE id = %s;"
#     cursor.execute(sql, (id,))
#     user = cursor.fetchone()
#
#     if user:
#         sql = "DELETE FROM users WHERE id = %s;"
#         cursor.execute(sql, (id,))
#         connection.commit()
#
#     return jsonify(user)
