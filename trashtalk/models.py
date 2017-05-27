from sqlalchemy import (create_engine,
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


def init_db():
    """
    Used to instantiate a new database. Must run from interpreter upon app setup!
    
    Import all modules here that might define models so that
    they will be registered properly on the metadata.  Otherwise
    you will have to import them first before calling init_db()
    
    :return: 
    """
    Base.metadata.create_all(bind=engine)

# MODELS

association_table = Table('participants', Base.metadata,
                          Column('cleanups_id', Integer, ForeignKey('cleanups.id')),
                          Column('users_id', String(250), ForeignKey('users.username')))


class Cleanup(Base):
    """
    Users can create Clean-up Events.
    """

    __tablename__ = 'cleanups'

    id = Column(Integer, primary_key=True)  # Computer Generated

    # Input at creation by user
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    street_number = Column(Integer, nullable=False)
    street_name = Column(String(250), nullable=False)
    image = Column(Text)  # Optional input

    # Program Assigned
    host_id = Column(String(250), ForeignKey('users.username'))
    city = Column(String(250))
    lat = Column(Numeric(10, 7))
    lng = Column(Numeric(10, 7))
    address = Column(Text)  # Set after geopy call
    html_url = Column(Text)  # Set after seeclickfix call

    # Many to Many: Cleanup and Participants, part 2 of 3
    participants = relationship('User',
                                secondary=association_table,
                                backref='cleanups_participated')


class User(Base):
    """
    Users can register.
    """

    __tablename__ = 'users'

    # required parameters to establish an account
    username = Column(String(250), primary_key=True)
    password = Column(String(250))
    authenticated = Column(Boolean, default=False)

    # optional profile parameters
    email = Column(String(250))
    volunteer_hours = Column(Numeric(6, 1))
    cleanups_hosted = relationship("Cleanup", backref='host')

    def hash_password(self):
        self.password = generate_password_hash(self.password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_active(self):
        return True

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated

    def is_annoymous(self):
        return False

