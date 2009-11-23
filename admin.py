from django.contrib import admin
from olwidget.admin import GeoModelAdmin

from world.models import WorldBorders

admin.site.register(WorldBorders, GeoModelAdmin)

