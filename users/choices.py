from django.db import models

class UserRoleChoice(models.TextChoices):
    ADMIN = ("admin", "admin")
    PROREKTOR = ("prorektor", "prorektor")
    BUGALTER = ("bugalter", "bugalter")
    XOJALIK = ("xojalik", "xojalik")
    RTTM = ("rttm", "rttm")
    OMBORCHI = ("omborchi", "omborchi")
    KOMENDANT = ("komendant", "komendant")

class MaxsulotRoleChoice(models.TextChoices):
    XOJALIK = ("xojalik", "xojalik")
    RTTM = ("rttm", "rttm")
