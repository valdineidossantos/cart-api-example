"""add product stock control

Revision ID: b66546b79cf8
Revises: 1d900699334c
Create Date: 2022-07-20 14:33:19.212953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b66546b79cf8'
down_revision = '1d900699334c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('quantity_stock', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'quantity_stock')
    # ### end Alembic commands ###