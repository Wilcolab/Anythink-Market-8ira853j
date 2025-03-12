"""create ratings table

Revision ID: 7a8df2b5c108
Revises: fdf8821871d7
Create Date: 2023-11-16
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7a8df2b5c108'
down_revision = 'fdf8821871d7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "ratings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("value", sa.Integer(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("item_id", sa.Integer(), nullable=False),  # Changed from UUID to Integer
        sa.Column("user_id", sa.Integer(), nullable=False),  # Changed from UUID to Integer
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["item_id"], ["items.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "item_id", name="unique_user_item_rating")
    )
    
    # Create index for faster lookups by item_id
    op.create_index(op.f("ix_ratings_item_id"), "ratings", ["item_id"], unique=False)
    
    # Create index for faster lookups by user_id
    op.create_index(op.f("ix_ratings_user_id"), "ratings", ["user_id"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_ratings_user_id"), table_name="ratings")
    op.drop_index(op.f("ix_ratings_item_id"), table_name="ratings")
    op.drop_table("ratings")
