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
    class RoleChoice(models.TextChoices):
        ADMIN = ("admin", "admin")
        PROREKTOR = ("prorektor", "prorektor")
        BUGALTER = ("bugalter", "bugalter")
        XOJALIK = ("xojalik", "xojalik")
        RTTM = ("rttm", "rttm")
        OMBORCHI = ("omborchi", "omborchi")
        KOMENDANT = ("komendant", "komendant")

    lavozim = models.CharField(max_length=255, blank=True)
    bino = models.ForeignKey(Binos, on_delete=models.CASCADE, null=True)
    qr_code = models.ImageField(upload_to='qr_code', null=True)
    qr_code_link = models.URLField(max_length=255, blank=True)
    parol = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=30, choices=RoleChoice.choices)

    def __str__(self):
        return self.username


# user = Users.role
# user = Users.RoleChoice.BUGALTER
