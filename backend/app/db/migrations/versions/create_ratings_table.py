"""create ratings table

Revision ID: 01aabbcc1122
Revises: <previous_revision_id>
Create Date: 2023-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01aabbcc1122'
down_revision = 'fdf8821871d7'  # replace with the previous migration ID
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    -- Add columns to items table
    ALTER TABLE items
    ADD COLUMN IF NOT EXISTS average_rating FLOAT,
    ADD COLUMN IF NOT EXISTS ratings_count INTEGER NOT NULL DEFAULT 0;
    
    -- Create ratings table
    CREATE TABLE IF NOT EXISTS ratings (
        id SERIAL PRIMARY KEY,
        value INTEGER NOT NULL,
        item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        comment TEXT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
        CONSTRAINT unique_user_item_rating UNIQUE(item_id, user_id)
    );
    """)


def downgrade():
    op.execute("""
    -- Drop ratings table
    DROP TABLE IF EXISTS ratings;
    
    -- Remove columns from items table
    ALTER TABLE items 
    DROP COLUMN IF EXISTS average_rating,
    DROP COLUMN IF EXISTS ratings_count;
    """)
