from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, EmailField, URLField
from wtforms.validators import DataRequired, URL, Email, Length, EqualTo


# User forms

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField(
        "Confirm", validators=[DataRequired(), EqualTo("password", message="Passwords must match")]
    )
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class UpdateUser(FlaskForm):
    username = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Update")


# Subreddit forms

class CreateSubreddit(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=3)])
    about = StringField("About", validators=[DataRequired(), Length(min=20)])
    submit = SubmitField("Create Subreddit")


class UpdateSubreddit(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=3)])
    about = StringField("About", validators=[DataRequired(), Length(min=20)])
    submit = SubmitField("Update Subreddit")


# Thread forms

class CreateThread(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=1)])
    content = StringField("Content", validators=[DataRequired(), Length(min=1)])
    submit = SubmitField("Post")


class UpdateThread(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=1)])
    content = StringField("Content", validators=[DataRequired(), Length(min=1)])
    submit = SubmitField("Update")


# Comment forms

class CreateComment(FlaskForm):
    content = StringField("Content", validators=[DataRequired(), Length(min=1)])
    submit = SubmitField("Post")


class UpdateComment(FlaskForm):
    content = StringField("Content", validators=[DataRequired(), Length(min=1)])
    submit = SubmitField("Update")


# Buttons

class Delete(FlaskForm):
    delete = SubmitField("Delete")


class Update(FlaskForm):
    update = SubmitField("Update")


class Join(FlaskForm):
    join = SubmitField("Join")


class Leave(FlaskForm):
    leave = SubmitField("Leave")
