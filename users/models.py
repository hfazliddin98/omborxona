import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    name = models.CharField(max_length=255, blank=True)
    superadmin = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    komendant = models.BooleanField(default=False)



class AsosiyModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = True)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)

    class Meta:
        abstract = True
