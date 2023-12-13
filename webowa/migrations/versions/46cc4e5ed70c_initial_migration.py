"""Initial migration

Revision ID: 46cc4e5ed70c
Revises: 
Create Date: 2023-12-13 19:38:44.919433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46cc4e5ed70c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('training',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('volume_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=20), nullable=False),
    sa.Column('volume', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('exercise',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('repetitions', sa.Integer(), nullable=False),
    sa.Column('sets', sa.Integer(), nullable=False),
    sa.Column('load', sa.Integer(), nullable=False),
    sa.Column('training_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['training_id'], ['training.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('training_exercises',
    sa.Column('training_id', sa.Integer(), nullable=True),
    sa.Column('exercise_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercise.id'], ),
    sa.ForeignKeyConstraint(['training_id'], ['training.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('training_exercises')
    op.drop_table('exercise')
    op.drop_table('volume_history')
    op.drop_table('training')
    # ### end Alembic commands ###
