from django.db import models
from django.utils import timezone
from autoslug import AutoSlugField
from django.utils.translation import gettext_lazy as _
from ..settings import AUTH_USER_MODEL
from django.contrib.auth import get_user_model


User = get_user_model()


class Event(models.Model):
    name = models.CharField(_("Event name"), max_length=100, blank=False, null=False)
    start = models.DateTimeField(_("Event start date"), blank=True, null=True)
    end = models.DateTimeField(_("Event end date"), blank=True, null=True)
    price = models.DecimalField(
        _("Event price"), max_digits=10, decimal_places=2, blank=True, null=True
    )
    picture = models.CharField(
        _("Event picture url"), max_length=200, blank=True, null=True
    )
    description = models.TextField(_("Event description"), blank=False, null=False)
    created = models.DateTimeField(default=timezone.now)
    slug = AutoSlugField(populate_from="name", unique=True)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    user_presences = models.ManyToManyField(
        AUTH_USER_MODEL, through="Presence", related_name="event_presences"
    )
    user_comments = models.ManyToManyField(
        AUTH_USER_MODEL, through="Comment", related_name="event_comments"
    )

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return self.name


class Presence(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(default=timezone.now)
    is_interested = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]
        unique_together = ("user", "event")

    def __str__(self) -> str:
        return f"{self.user} @ {self.event}"


class Comment(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    body = models.TextField(_("Comment text"))

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return self.body
