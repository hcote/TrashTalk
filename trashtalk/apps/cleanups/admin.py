from django.contrib import admin

from .models import Cleanup, Location

# Register your models here.
admin.site.register(Cleanup)
admin.site.register(Location)
