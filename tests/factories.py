import factory

from trashtalk.models import db_session, User, Cleanup


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db_session
        model = User

    username = factory.Sequence(lambda n: 'TestUser %s' % n)
    password = 'password'
