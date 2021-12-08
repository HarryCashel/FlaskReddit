from main import ma
from models.Thread import Comment
from marshmallow.validate import Length


class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment

    content = ma.String(required=True, validate=Length(min=1))
    # comments = ma.Nested(comments_schema)


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
