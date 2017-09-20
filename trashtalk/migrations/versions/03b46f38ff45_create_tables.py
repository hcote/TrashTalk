"""create tables

Revision ID: 03b46f38ff45
Revises: 
Create Date: 2017-09-15 17:42:55.841186

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import relationship as rel

# revision identifiers, used by Alembic.
revision = '03b46f38ff45'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create Cleanup table
    op.create_table(
        'cleanups',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created', sa.DateTime, default=sa.func.now()),
        sa.Column('modified', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('name', sa.String(length=250)),
        sa.Column('description', sa.Text),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('start_time', sa.Time, nullable=False),
        sa.Column('end_time', sa.Time, nullable=False),
        sa.Column('image', sa.Text, default='default_broom.png'),
        sa.Column('host_id', sa.ForeignKey('users.id')),
        sa.Column('location_id', sa.ForeignKey('locations.id')),
        sa.Column('html_url', sa.Text),
        sa.Column('notified_pw', sa.Boolean, default=False),
        sa.Column('participants', rel('User', backref='location'))
    )
    # Create Location table
    op.create_table(
        'locations',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created', sa.DateTime, default=sa.func.now()),
        sa.Column('modified', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('number', sa.String),
        sa.Column('street', sa.String),
        sa.Column('cross_street', sa.String),
        sa.Column('city', sa.String),
        sa.Column('state', sa.String),
        sa.Column('zipcode', sa.String),
        sa.Column('county', sa.String),
        sa.Column('district', sa.String),
        sa.Column('country', sa.String),
        sa.Column('latitude', sa.String),
        sa.Column('longitude', sa.String),
        sa.Column('cleanups', rel('Cleanup', backref='location'))
    )
    # Create User table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created', sa.DateTime, default=sa.func.now()),
        sa.Column('modified', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('username', sa.String(length=250)),
        sa.Column('password', sa.String(length=250)),
        sa.Column('authenticated', sa.Boolean, default=False),
        sa.Column('email', sa.String(length=250)),
        sa.Column('volunteer_hours', sa.Numeric(6, 1)),
        sa.Column('cleanups', rel('Cleanup', backref='host'))
    )


def downgrade():
    pass
