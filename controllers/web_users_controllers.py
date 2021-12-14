from models.User import User
from main import db
from schemas.UserSchema import user_schema
from flask import Blueprint, render_template, flash, redirect, url_for, abort, request
from flask_login import current_user, login_user, logout_user, login_required

web_users = Blueprint("web_users", __name__, url_prefix="/web")

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None