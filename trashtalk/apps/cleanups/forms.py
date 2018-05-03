from django.forms import ModelForm, inlineformset_factory, modelformset_factory

from .models import Cleanup, Location


class CleanupForm(ModelForm):
    class Meta:
        model = Cleanup
        fields = ('title', 'description', 'start', 'end', 'image', 'host')


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ('number', 'street', 'cross_street')


# Locations can have many cleanups ...or can they ...
CleanupFormSet = inlineformset_factory(Location, Cleanup, form=CleanupForm,
                                       extra=1, max_num=1)
