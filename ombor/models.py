from django.db import models
from users.models import AsosiyModel, Users


class Kategoriya(AsosiyModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class MaxsulotNomi(AsosiyModel):
    kategoriya = models.ForeignKey(Kategoriya, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Birlik(AsosiyModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class OmborniYopish(AsosiyModel):
    yopish = models.BooleanField(default=False)

    def __str__(self):
        return self.yopish

class Ombor(AsosiyModel):
    kategoriya = models.ForeignKey(Kategoriya, on_delete=models.CASCADE)
    maxsulot_nomi = models.ForeignKey(MaxsulotNomi, on_delete=models.CASCADE)
    qiymat = models.CharField(max_length=255)
    birlik = models.ForeignKey(Birlik, on_delete=models.CASCADE)
    maxviylik = models.BooleanField(default=False)

    def __str__(self):
        return self.kategoriya 

class Korzinka(AsosiyModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    kategoriya = models.ForeignKey(Kategoriya, on_delete=models.CASCADE)
    maxsulot_nomi = models.ForeignKey(MaxsulotNomi, on_delete=models.CASCADE)
    qiymat = models.CharField(max_length=255)
    birlik = models.ForeignKey(Birlik, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.kategoriya

class OlinganMaxsulotlar(AsosiyModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    kategoriya = models.ForeignKey(Kategoriya, on_delete=models.CASCADE)
    maxsulot_nomi = models.ForeignKey(MaxsulotNomi, on_delete=models.CASCADE)
    qiymat = models.CharField(max_length=255)
    birlik = models.ForeignKey(Birlik, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.kategoriya
