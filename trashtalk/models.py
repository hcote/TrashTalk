from sqlalchemy import (create_engine, func, DateTime,
                        Column, Date, Time, Integer,
                        Numeric, ForeignKey, String,
                        Text, Boolean, Table)
from sqlalchemy.exc import DataError, DatabaseError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash

from trashtalk.constants import (DEFAULT_CITY, DEFAULT_STATE,
                                 STATE_CODE_MAP, COUNTRY_CODE_MAP)
from trashtalk.settings import app
from trashtalk.utils import Point

# DATABASE CONFIGURATION
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=False)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


# Database Utilities
def init_db():
    """
    Used to instantiate a new database. Must run from interpreter upon app setup!
    
    Import all modules here that might define models so that
    they will be registered properly on the metadata.  Otherwise
    you will have to import them first before calling init_db()
    
    :return: 
    """
    Base.metadata.create_all(bind=engine)

"""
About SQLAlchemy Models and Relationships
-----------------------------------------

Reference: http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html

SQLA will automatically update relations in the association table as new objects tracked
within it are updated. When a user joins a new cleanup, that association will be 
reflected in the participants_table.
"""

participants_table = Table('participants', Base.metadata,
                           Column('cleanups_id', Integer, ForeignKey('cleanups.id')),
                           Column('users_id', Integer, ForeignKey('users.id')))


class Model(Base):
    """
    Default fields and functions for all models
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True)
    modified = Column(DateTime, default=func.now(), onupdate=func.now())
    created = Column(DateTime, default=func.now())

    def save(self):
        """
        Stores model instances. If any errors occur, rollback the change.

        :return:
        """
        try:
            db_session.add(self)
            db_session.commit()
        except (DataError, DatabaseError):
            app.logger.exception("Failed to save.")
            db_session.rollback()

    def update(self, **attrs):
        """
        Updates a model instance by checking for changes in attributes. Will only
        update changes.

        :param attrs: `dict`, updated attributes
        :return:
        """
        app.logger.info("Updating model: %s | %s", self.id, attrs)
        try:
            for k, v in attrs.items():
                app.logger.info("Model attr: %s\nval: %s", k, v)
                if hasattr(self, k) and not v == getattr(self, k):
                    if v == '':
                        setattr(self, k, None)
                    else:
                        setattr(self, k, v)
                else:
                    app.logger.info("Skipping attr: %s", k)
                    continue
        except (DataError, DatabaseError):
            app.logger.exception("Could not update Cleanup.")
            db_session.rollback()
        else:
            self.save()

    def delete(self):
        try:
            db_session.delete(self)
            db_session.commit()
        except DatabaseError:
            app.logger.exception("Delete Cleanup failed: %s", self.id)
        else:
            app.logger.info("Cleanup deleted successfully")


class Cleanup(Model):
    """
    Users can create Clean-up Events.
    """

    __tablename__ = 'cleanups'

    # Input at creation by user
    name = Column(String(250))  # Optional; defaults to location address
    description = Column(Text)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    image = Column(Text, default='default_broom.png')  # Optional input

    # Program Assigned
    host_id = Column(Integer, ForeignKey('users.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    html_url = Column(Text)  # Set after seeclickfix call

    # Many to Many: Cleanup and Participants, part 2 of 3
    participants = relationship('User',
                                secondary=participants_table,
                                backref='cleanups_participated')

    def __str__(self):
        return "Cleanup at {0}".format(self.location)

    @property
    def gmap_query(self):
        """For cross street queries."""
        if self.location and self.location.cross_street:
            return "{0}:{1}, {2}".format(self.location.street,
                                         self.location.cross_street, self.city)
        else:
            return self.address

    @property
    def address(self):
        return "{0} {1}, {2} {3}".format(self.location.street,
                                         self.location.city, self.location.state,
                                         self.location.zipcode)

    def check_name(self):
        if not self.name:
            self.name = self.location


class User(Model):
    """
    Users can register.
    """

    __tablename__ = 'users'

    # required parameters to establish an account
    username = Column(String(250))
    password = Column(String(250))
    authenticated = Column(Boolean, default=False)

    # optional profile parameters
    email = Column(String(250))
    volunteer_hours = Column(Numeric(6, 1))
    cleanups = relationship("Cleanup", backref="host")

    def hash_password(self):
        self.password = generate_password_hash(self.password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update_password(self, password):
        self.password = generate_password_hash(password)

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_annoymous(self):
        return False


class Location(Model):
    __tablename__ = 'locations'

    number = Column(String)
    street = Column(String(250))
    cross_street = Column(String(250))
    city = Column(String(250), default=DEFAULT_CITY)
    state = Column(String(250), default=DEFAULT_STATE)
    zipcode = Column(String(10))
    county = Column(String(250))
    district = Column(String(250))
    country = Column(String(250))
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))

    cleanups = relationship('Cleanup', backref='location')

    def __str__(self):
        return "{0} {1}, {2}".format(self.street, self.cross_street, self.city)

    @property
    def address(self):
        return "{} {}".format(self.number, self.street)

    @property
    def coordinates(self):
        return Point(self.latitude, self.longitude)

    @property
    def state_code(self):
        if not self.has_state_code():
            return STATE_CODE_MAP[self.state]
        return self.state

    @property
    def country_code(self):
        if not self.has_country_code():
            self.country = COUNTRY_CODE_MAP[self.country]
        return self.country

    def has_country_code(self):
        return len(self.country) < 3

    def has_state_code(self):
        return len(self.state) < 3


# Migration utilities
# Use to update current database entries to reflect model changes.
def add_default_images(img):
    """Add default images to cleanups for which no image was provided."""
    cleanups = db_session.query(Cleanup).filter(Cleanup.image == '')
    for cleanup in cleanups:
        cleanup.image = img
        db_session.add(cleanup)
    db_session.commit()


def add_default_city(city):
    objs = db_session.query(Cleanup).filter(Cleanup.city == '')
    for o in objs:
        o.city = city
        db_session.add(o)
    db_session.commit()
