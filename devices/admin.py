from django.contrib import admin

from django.contrib import admin
from .models import Device, DataEntry, Project

admin.site.register(Device)
admin.site.register(DataEntry)
admin.site.register(Project)