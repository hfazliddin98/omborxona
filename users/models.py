import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    name = models.CharField(max_length=255, blank=True)
    superadmin = models.BooleanField(default=False)
    prorektor = models.BooleanField(default=False)
    bugalter = models.BooleanField(default=False)
    xojalik_bolimi = models.BooleanField(default=False)
    it_park = models.BooleanField(default=False)
    omborchi = models.BooleanField(default=False)
    komendant = models.BooleanField(default=False)
    parol = models.CharField(max_length=255, blank=True)



class AsosiyModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = True)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)

    class Meta:
        abstract = True
