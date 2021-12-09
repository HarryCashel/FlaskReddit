from main import ma
from models.Subreddit import Subreddit
from schemas.ThreadSchema import threads_schema
from marshmallow.validate import Length


class SubredditSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Subreddit

    name = ma.String(required=True)
    content_about = ma.String(required=True, validate=Length(min=1))

    threads = ma.Nested(threads_schema)


subreddit_schema = SubredditSchema()
subreddits_schema = SubredditSchema(many=True)
