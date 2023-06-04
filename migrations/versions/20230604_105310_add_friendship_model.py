"""add friendship model

Revision ID: 475b958a9452
Revises: 0376553609e4
Create Date: 2023-06-04 10:53:10.793574

"""
from alembic import op
import sqlalchemy as sa

import os
environment = os.getenv("FLASK_ENV")
SCHEMA = os.environ.get("SCHEMA")


# revision identifiers, used by Alembic.
revision = '475b958a9452'
down_revision = '0376553609e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('friendships',
    sa.Column('userA_id', sa.Integer(), nullable=False),
    sa.Column('userB_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['userA_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['userB_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('userA_id', 'userB_id')
    )
    # ### end Alembic commands ###

    if environment == "production":
      op.execute(f"ALTER TABLE friendships SET SCHEMA {SCHEMA};")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('friendships')
    # ### end Alembic commands ###
