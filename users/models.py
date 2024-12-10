import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser




class AsosiyModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = True)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)

    class Meta:
        abstract = True

class Binos(AsosiyModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Users(AbstractUser):
    name = models.CharField(max_length=255, blank=True)
    bino = models.ForeignKey(Binos, on_delete=models.CASCADE, null=True)
    superadmin = models.BooleanField(default=False)
    prorektor = models.BooleanField(default=False)
    bugalter = models.BooleanField(default=False)
    xojalik_bolimi = models.BooleanField(default=False)
    it_park = models.BooleanField(default=False)
    omborchi = models.BooleanField(default=False)
    komendant = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr_code', null=True)
    qr_code_link = models.URLField(max_length=255, blank=True)
    parol = models.CharField(max_length=255, blank=True)

