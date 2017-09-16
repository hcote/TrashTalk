"""add locations

Location data was formerly stored on the Cleanup model. Removes location data from the
Cleanup model and creates a new model, Locations to keep all locational data.

Revision ID: 9248fbf8f01e
Revises: 
Create Date: 2017-06-26 08:34:03.546812

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.orm.relationship as rel


# revision identifiers, used by Alembic.
revision = '9248fbf8f01e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add new name and escription column
    op.add_column('cleanups', sa.Column('name', sa.String))
    op.add_column('cleanups', sa.Column('description', sa.Text))

    # Create new table: Location
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
    # Add location relation
    op.add_column('cleanups', sa.Column('location_id', sa.ForeignKey('locations.id')))


def downgrade():
    # Remove all location data from Cleanup
    op.drop_column('cleanups', 'number')
    op.drop_column('cleanups', 'street_name')
    op.drop_column('cleanups', 'street_number')
    op.drop_column('cleanups', 'lat')
    op.drop_column('cleanups', 'lng')
    op.drop_column('cleanups', 'city')
    op.drop_column('cleanups', 'state')
    op.drop_column('cleanups', 'zipcode')
    op.drop_column('cleanups', 'county')
    op.drop_column('cleanups', 'district')
    op.drop_column('cleanups', 'country')

