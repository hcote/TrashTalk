from django.contrib import admin

from .models import Cleanup, Location, RequiredTool, Tool, ToolCategory

# pylint: disable=missing-docstring
class ToolAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ['category']


# Register your models here.
admin.site.register(Cleanup)
admin.site.register(Location)
admin.site.register(RequiredTool)
admin.site.register(Tool, ToolAdmin)
admin.site.register(ToolCategory)
