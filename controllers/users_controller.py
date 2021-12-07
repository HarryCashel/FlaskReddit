from flask import Blueprint, request, jsonify
from main import db
from models.User import User
from schemas.UserSchema import user_schema, users_schema
from flask_migrate import Migrate

users = Blueprint("users", __name__, url_prefix="/users")


@users.route("/", methods=["GET"])
def user_index():
    # Return all users
    users = User.query.all()
    
    return jsonify(users_schema.dump(users))


@users.route("/", methods=["POST"])
def user_create():
    # Create a new user
    user_fields = user_schema.loads(request.json)
    new_user = User()
    new_user.username = user_fields["username"]
    new_user.email = user_fields["email"]
    new_user.password = user_fields["password"]

    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user))

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
