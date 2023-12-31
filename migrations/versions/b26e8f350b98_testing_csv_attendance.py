"""testing csv attendance

Revision ID: b26e8f350b98
Revises: 158e4c81e1ac
Create Date: 2023-08-04 09:53:38.157795

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b26e8f350b98'
down_revision = '158e4c81e1ac'
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
    op.drop_table('persontestcsv')
    op.drop_table('meetingtestcsv')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('meetingtestcsv',
    sa.Column('MeetingTestID', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('StartDate', sa.DATE(), nullable=True),
    sa.Column('StartTime', mysql.TIME(), nullable=True),
    sa.Column('EndDate', sa.DATE(), nullable=True),
    sa.Column('EndTime', mysql.TIME(), nullable=True),
    sa.Column('Title', mysql.VARCHAR(length=256), nullable=True),
    sa.PrimaryKeyConstraint('MeetingTestID'),
    mysql_collate='latin1_swedish_ci',
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.create_table('persontestcsv',
    sa.Column('PersonTestID', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('FirstName', mysql.VARCHAR(length=256), nullable=True),
    sa.Column('LastName', mysql.VARCHAR(length=256), nullable=True),
    sa.Column('Email', mysql.VARCHAR(length=256), nullable=True),
    sa.PrimaryKeyConstraint('PersonTestID'),
    mysql_collate='latin1_swedish_ci',
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.drop_table('personTestCSV')
    op.drop_table('meetingTestCSV')
    # ### end Alembic commands ###
