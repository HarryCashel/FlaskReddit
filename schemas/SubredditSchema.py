from main import ma
from models.Subreddit import Subreddit
from models.SubredditMembers import SubredditMembers
from schemas.ThreadSchema import threads_schema, ThreadSchema
from schemas.UserSchema import UserSchema
from marshmallow.validate import Length


class SubredditSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Subreddit

    name = ma.String(required=True)
    description = ma.String(required=True, validate=Length(min=1))

    user = ma.Nested(UserSchema)
    threads = ma.Nested(ThreadSchema)


class SubredditMembersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SubredditMembers

    user_id = ma.String()
    subreddit_id = ma.String()


subreddit_schema = SubredditSchema()
subreddits_schema = SubredditSchema(many=True)

subreddit_member_schema = SubredditMembersSchema()
subreddit_members_schema = SubredditMembersSchema(many=True)
