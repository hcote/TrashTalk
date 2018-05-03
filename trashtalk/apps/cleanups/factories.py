import factory
import factory.faker
import factory.fuzzy

from core.utils import iso_time
from .models import Cleanup, Location, User


# pylint: disable=missing-docstring
class UserFactory(factory.DjangoModelFactory):
    # pylint: disable=too-few-public-methods
    class Meta:
        model = User

    username = factory.Faker('name')
    first_name = factory.Faker('name')
    last_name = factory.Faker('name')
    password = 'password'
    email = factory.LazyAttribute(lambda u: '%s@example.com' % u.username)


# pylint: disable=missing-docstring
class LocationFactory(factory.DjangoModelFactory):
    # pylint: disable=too-few-public-methods
    class Meta:
        model = Location

    number = '2323'
    street = 'Broadway'
    cross_street = '23rd'


# pylint: disable=missing-docstring
class CleanupFactory(factory.DjangoModelFactory):
    # pylint: disable=too-few-public-methods
    class Meta:
        model = Cleanup

    title = factory.fuzzy.FuzzyText(prefix='Cleanup-')
    description = factory.Sequence(lambda n: 'Cleanup number %s needs YOU!' % n)
    start = '2018-04-15 15:30'
    end = '2018-04-15 17:30'
    host = factory.SubFactory(UserFactory)
    location = factory.SubFactory(LocationFactory)


def cleanup_factory(request):
    location_data = {'street': request.pop('street')[0], 'number': request.pop('number')[0]}
    cleanup = {
        'title': request.get('title'),
        'description': request.get('description'),
        'start': iso_time(request.get('start')),
        'end': iso_time(request.get('end')),
        'image': request.get('image', Cleanup.DEFAULT_ICON),
        'host': User.objects.get(username=request.get('host')),
        'location': location_data
    }
    return cleanup
