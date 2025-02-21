import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from .choices import UserRoleChoice




class AsosiyModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = False)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)

    class Meta:
        abstract = True

class Binos(AsosiyModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Users(AbstractUser):
    lavozim = models.CharField(max_length=255, blank=True)
    bino = models.ForeignKey(Binos, on_delete=models.CASCADE, null=True)
    qr_code = models.ImageField(upload_to='qr_code', null=True)
    qr_code_link = models.URLField(max_length=255, blank=True)
    parol = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=30, choices=UserRoleChoice.choices)

    def __str__(self):
        return self.username



