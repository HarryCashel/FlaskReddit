from main import ma
from models.User import User
from marshmallow.validate import Length, Email


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

    email = ma.String(required=True, validate=Email())
    username = ma.String(required=True, validate=Length(min=3))
    password = ma.String(required=True, validate=Length(min=8))


user_schema = UserSchema()
users_schema = UserSchema(many=True)
