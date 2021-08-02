from django.contrib import admin
from django.db.models.fields import PositiveSmallIntegerField
from .models import Event, Presence, Comment

admin.site.register(Event)
admin.site.register(Presence)
admin.site.register(Comment)