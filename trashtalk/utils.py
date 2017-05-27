__author__ = "miller.tim"
__date__ = "$Mar 31, 2017 11:25:41 PM$"

from sqlalchemy import Column, Date, Time, Integer, Numeric, ForeignKey
from sqlalchemy import String, Text, create_engine, Boolean, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship  # , sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

# SQL Connection parameters
SQL_HOST = ""
SQL_PASSWORD = ""
SQL_IP_ADDRESS = ""
SQL_DATABASE = ""

# Access SQL, using pymysql
engine = create_engine('mysql+pymysql://%s:%s@%s/%s' % (
SQL_HOST, SQL_PASSWORD, SQL_IP_ADDRESS, SQL_DATABASE))
Base = declarative_base()

# Many to Many, relationship between a cleanup and its participants; part 1 of 3
association_table = Table('participants', Base.metadata,
                          Column('cleanups_id', Integer, ForeignKey('cleanups.id')),
                          Column('users_id', String(250), ForeignKey('users.username'))
                          )


# SQL Structure from Cleanups
# SQLAlchemy allows programmers to interact with SQL like objects
class Cleanup(Base):
    __tablename__ = 'cleanups'
    # Key
    id = Column(Integer, primary_key=True)  # Computer Generated

    # Input at creation by user
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    street_number = Column(Integer, nullable=False)
    street_name = Column(String(250), nullable=False)
    image = Column(Text)  # Optional input

    # Program Assigned
    host_id = Column(String(250), ForeignKey(
        'users.username'))  # One to Many Relationship: One user to host Many cleanups,
    #  part 1 of 2
    city = Column(String(250))  # Never set because global variable from Main used instead
    lat = Column(Numeric(10, 7))
    lng = Column(Numeric(10, 7))
    address = Column(Text)  # Set after geopy call
    html_url = Column(Text)  # Set after seeclickfix call

    # Many to Many: Cleanup and Participants, part 2 of 3
    participants = relationship('User',
                                secondary=association_table,
                                backref='cleanups_participated')  # part 3 of 3 (creates relationship in User)


class User(Base):
    __tablename__ = 'users'

    # required parameters to establish an account
    username = Column(String(250), primary_key=True)
    password = Column(String(250))
    authenticated = Column(Boolean, default=False)

    # optional profile parameters
    email = Column(String(250))
    volunteer_hours = Column(Numeric(6, 1))
    cleanups_hosted = relationship("Cleanup",
                                   backref='host')  # One to many relationship, part 2
    # of 2

    # Security Features and Account management tools, required by Flask login tool
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


# Create database with structure outlined above
Base.metadata.create_all(engine)


# Send Base and Engine to Main
def getBase():
    return Base


def getEngine():
    return engine
