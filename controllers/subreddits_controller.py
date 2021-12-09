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
from schemas.SubredditSchema import threads_schema

subreddits = Blueprint("subreddits", __name__, url_prefix="/subreddits")




