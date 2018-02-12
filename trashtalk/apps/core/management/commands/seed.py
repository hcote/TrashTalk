from faker import Faker

from django.core.management.base import BaseCommand

from cleanups.models import User, Cleanup, Location


class Command(BaseCommand):
    help = 'Seed the project with data for demos only.'

    def add_arguments(self, parser):
        parser.add_argument('csv')
        parser.add_argument('--amount', dest='amount', default=15, type=int)

    def handle(self, *args, **options):
        print("Seeding database ...\n\n")
        fake = Faker()

        # Create locations
        path = options['csv']
        amount = int(options['amount'])
        file = open(path)
        location_data = [line for line in file]
        cols = location_data.pop(0).strip().lower().split(',')

        addresses = []
        print("Creating locations...")
        for row in location_data[:amount]:
            data = row.strip().split(',')
            loc = dict(zip(cols, data))
            addresses.append(loc)
        print("\tLocations parsed: ", len(addresses))

        for address in addresses:
            # Create all the locations
            location = Location.objects.create(street=address['block'],
                                          zipcode=address['zipcode'],
                                          category='address')

            # Create a user
            user = User.objects.create_user(fake.user_name(), fake.email(), 'password')

            # Create cleanup using location and user
            Cleanup.objects.create(title="Cleanup Event at {}".format(location),
                                   description="Grab a broom!",
                                   start_time='3:30 PM',
                                   end_time='7:30PM',
                                   date='2020-03-12',
                                   host=user,
                                   location=location)
        print("Added {} cleanups.".format(Cleanup.objects.count()))
