from django.db import models
from decimal import Decimal
from users.models import AsosiyModel, Users


class Kategoriya(AsosiyModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Maxsulot(AsosiyModel):
    kategoriya = models.ForeignKey(Kategoriya, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    maxviylik = models.BooleanField(default=False)
    
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
    maxsulot = models.ForeignKey(Maxsulot, on_delete=models.CASCADE)
    qiymat = models.DecimalField(max_digits=10, decimal_places=2) 
    birlik = models.ForeignKey(Birlik, on_delete=models.CASCADE)


    def __str__(self):
        return self.maxsulot.name 
    
class JamiMahsulot(AsosiyModel):
    maxsulot = models.ForeignKey(Maxsulot, on_delete=models.CASCADE)
    qiymat = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00')) 
    birlik = models.ForeignKey(Birlik, on_delete=models.CASCADE)


    def __str__(self):
        return self.maxsulot.name 
        
    
class Buyurtma(AsosiyModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    sorov = models.BooleanField(default=False)
    tasdiq = models.BooleanField(default=False)
    rad = models.BooleanField(default=False)

    def __str__(self):
        return self.user   

class Korzinka(AsosiyModel):
    buyurtma = models.ForeignKey(Buyurtma, on_delete=models.CASCADE)
    maxsulot = models.ForeignKey(Maxsulot, on_delete=models.CASCADE)
    qiymat = models.DecimalField(max_digits=10, decimal_places=2) 
    birlik = models.ForeignKey(Birlik, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.maxsulot.name

class OlinganMaxsulotlar(AsosiyModel):
    buyurtma = models.ForeignKey(Buyurtma, on_delete=models.CASCADE)
    maxsulot = models.ForeignKey(Maxsulot, on_delete=models.CASCADE)
    qiymat = models.DecimalField(max_digits=10, decimal_places=2) 
    birlik = models.ForeignKey(Birlik, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.maxsulot.name
