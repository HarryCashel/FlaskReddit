from main import ma
from models.Thread import Thread
from schemas.CommentSchema import comments_schema
from marshmallow.validate import Length


class ThreadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Thread

    title = ma.String(required=True, validate=Length(min=1))
    content = ma.String(required=True, validate=Length(min=1))

    comments = ma.Nested(comments_schema)


thread_schema = ThreadSchema()
threads_schema = ThreadSchema(many=True)
