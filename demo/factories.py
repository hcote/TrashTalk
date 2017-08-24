from trashtalk.models import *
from input_handling import twenty_four_time



def location_factory(data):
    location = Location(
        number=data.get('address'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude')
        # number=data.get('number'),
        # street=data.get('street'),
        # cross_street=data.get('cross_street'),
        # city=data.get('city'),
        # state=data.get('state'),
        # zipcode=data.get('zipcode'),
        # county=data.get('county'),
        # district=data.get('district'),
        # country=data.get('country')
    )
    location.save()
    return location


def cleanup_factory(data):
    #TDO-DO: Move to more appropriate location
    twenty_four_start = twenty_four_time(data.get("start_time"), data.get("start_time_of_day"))
    twenty_four_end = twenty_four_time(data.get("end_time"), data.get("end_time_of_day"))

    cleanup = Cleanup(
        #SQL does not currently handle the commented out values

        name=data.get('name'),
        description=data.get('description'),
        location=data.get('location'),
        date=data.get('date'),
        start_time=twenty_four_start,
        end_time=twenty_four_end,
        #street_name=data.get('street_name'),
        #street_number=data.get('street_number'),
        #cross_street_name=data.get('cross_street_name'),
        image=data.get('image'),
        host=data.get('host')#, added variable
        #city=data.get('city'),
        #state=data.get('state'),
        #zipcode=data.get('zipcode'),
        #county=data.get('county'),
        #district=data.get('district'),
        #country=data.get('country'),
    )
    print("Image: ",data.get('image'))
    cleanup.save()
    return cleanup


def user_factory(**data):
    user = User(
        username=data.get('username'),
        password=data.get('password'),
        email=data.get('email')
    )
    user.save()
    return user
