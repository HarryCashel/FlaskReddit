"""update user schema to not require username

Revision ID: 8f1baa994954
Revises: 
Create Date: 2021-12-09 13:56:23.030768

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f1baa994954'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password', sa.String(length=1000), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('role', sa.SmallInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('subreddits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('content_about', sa.String(length=1000), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('subreddit_members',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('subreddit_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['subreddit_id'], ['subreddits.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'subreddit_id')
    )
    op.create_table('threads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('content', sa.String(length=1000), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('thread_owner', sa.Integer(), nullable=True),
    sa.Column('parent_subreddit', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_subreddit'], ['subreddits.id'], ),
    sa.ForeignKeyConstraint(['thread_owner'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=1000), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('parent_thread', sa.Integer(), nullable=True),
    sa.Column('comment_owner', sa.Integer(), nullable=True),
    sa.Column('parent_comment', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['comment_owner'], ['users.id'], ),
    sa.ForeignKeyConstraint(['parent_comment'], ['comments.id'], ),
    sa.ForeignKeyConstraint(['parent_thread'], ['threads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    op.drop_table('threads')
    op.drop_table('subreddit_members')
    op.drop_table('subreddits')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###