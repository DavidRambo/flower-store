"""add bloom and height to flower

Revision ID: 5cd1b438f03b
Revises: 83aa792acbc1
Create Date: 2023-05-09 09:14:42.912377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cd1b438f03b'
down_revision = '83aa792acbc1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flower', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bloom_size', sa.Float(precision=5), nullable=True))
        batch_op.add_column(sa.Column('height', sa.Float(precision=5), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flower', schema=None) as batch_op:
        batch_op.drop_column('height')
        batch_op.drop_column('bloom_size')

    # ### end Alembic commands ###
