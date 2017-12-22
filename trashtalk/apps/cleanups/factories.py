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
    start_time = '15:30 PM'
    end_time = '17:30 PM'
    host = factory.SubFactory(UserFactory)
    location = factory.SubFactory(LocationFactory)


def cleanup_factory(request):
    location_data = {'street': request.pop('street')[0], 'number': request.pop('number')[0]}
    cleanup = {
        'title': request.get('title'),
        'description': request.get('description'),
        'date': request.get('date'),
        'start_time': iso_time(request.get('start_time')),
        'end_time': iso_time(request.get('end_time')),
        'image': request.get('image'),
        'host': User.objects.get(username=request.get('host')),
        'location': location_data
    }
    return cleanup
