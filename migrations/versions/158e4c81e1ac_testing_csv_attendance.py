"""testing csv attendance

Revision ID: 158e4c81e1ac
Revises: 0aaed4e2832f
Create Date: 2023-08-04 09:47:00.984059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '158e4c81e1ac'
down_revision = '0aaed4e2832f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('meetingTestCSV',
    sa.Column('MeetingTestID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('StartDate', sa.Date(), nullable=True),
    sa.Column('StartTime', sa.Time(), nullable=True),
    sa.Column('EndDate', sa.Date(), nullable=True),
    sa.Column('EndTime', sa.Time(), nullable=True),
    sa.Column('Title', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('MeetingTestID')
    )
    op.create_table('personTestCSV',
    sa.Column('PersonTestID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('FirstName', sa.String(length=256), nullable=True),
    sa.Column('LastName', sa.String(length=256), nullable=True),
    sa.Column('Email', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('PersonTestID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('personTestCSV')
    op.drop_table('meetingTestCSV')
    # ### end Alembic commands ###
