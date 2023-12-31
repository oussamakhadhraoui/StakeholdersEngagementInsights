"""removal of zone from meeting

Revision ID: e10aa68913fa
Revises: 2ec87fba6544
Create Date: 2023-08-15 14:16:58.181412

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e10aa68913fa'
down_revision = '2ec87fba6544'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('meeting', schema=None) as batch_op:
        batch_op.drop_constraint('meeting_ibfk_2', type_='foreignkey')
        batch_op.drop_column('ZoneID')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('meeting', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ZoneID', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('meeting_ibfk_2', 'zone', ['ZoneID'], ['ZoneID'])

    # ### end Alembic commands ###
