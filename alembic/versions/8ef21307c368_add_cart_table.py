"""add cart table

Revision ID: 8ef21307c368
Revises: 1c692720430e
Create Date: 2022-07-20 21:49:52.666213

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "8ef21307c368"
down_revision = "1c692720430e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "carts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finish_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_carts_id"), "carts", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_carts_id"), table_name="carts")
    op.drop_table("carts")
    # ### end Alembic commands ###
