from sqlalchemy import (create_engine, func, DateTime,
                        Column, Date, Time, Integer,
                        Numeric, ForeignKey, String,
                        Text, Boolean, Table)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash

from trashtalk.settings import app


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
        db_session.add(self)
        db_session.commit()

    def update(self, data):
        for k, v in data.items():
            if k in self.fields:
                setattr(self, k, v)
        self.save()


class Cleanup(Model):
    """
    Users can create Clean-up Events.
    """

    __tablename__ = 'cleanups'
    fields = ['date', 'start_time', 'end_time',
              'street_number', 'street_name', 'image',
              'city', 'lat', 'lng', 'address', 'html_url', 'participants']

    # Input at creation by user
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    street_number = Column(Integer, nullable=False)
    street_name = Column(String(250), nullable=False)
    image = Column(Text, default='default_broom.png')  # Optional input

    # Program Assigned
    host_id = Column(Integer, ForeignKey('users.id'))
    city = Column(String(250))
    lat = Column(Numeric(10, 7))
    lng = Column(Numeric(10, 7))
    address = Column(Text)  # Set after geopy call
    html_url = Column(Text)  # Set after seeclickfix call

    # Many to Many: Cleanup and Participants, part 2 of 3
    participants = relationship('User',
                                secondary=participants_table,
                                backref='cleanups_participated')


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


# Migration utilities
# Use to update current database entries to reflect model changes.
def add_default_images(img):
    cleanups = db_session.query(Cleanup).filter(Cleanup.image == None)
    for cleanup in cleanups:
        cleanup.image = img
    db_session.add_all(cleanups)
    db_session.commit()
