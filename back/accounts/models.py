from django.contrib.auth.models import AbstractUser
from django.db import models
from autoslug import AutoSlugField

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    birthday = models.DateTimeField(blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    slug = AutoSlugField(populate_from='username', unique=True)
    picture = models.CharField(max_length=200, blank=True, null=True)
    is_staff = models.BooleanField(default=False) 
    is_producer = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
