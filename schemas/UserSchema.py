from main import ma
from models.User import User
from marshmallow.validate import Length, Email


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        # only store password on serialisation, on deserialization - strip it out. - Do not save
        # prevents leaking the hashed password
        load_only = ["password"]

    email = ma.String(required=True, validate=[Email(), Length(min=4)])
    username = ma.String(validate=Length(min=3))
    password = ma.String(required=True, validate=Length(min=8))


user_schema = UserSchema()
users_schema = UserSchema(many=True)
