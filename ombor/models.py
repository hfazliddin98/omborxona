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
    it_park = models.BooleanField(default=False)
    
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
    qiymat = models.DecimalField(max_digits=10, decimal_places=1, default=Decimal('0.00')) 
    birlik = models.ForeignKey(Birlik, on_delete=models.CASCADE)


    def __str__(self):
        return self.maxsulot.name 
        
    
class Buyurtma(AsosiyModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    sorov = models.BooleanField(default=False)
    prorektor = models.BooleanField(default=False)
    bugalter = models.BooleanField(default=False)
    xojalik_bolimi = models.BooleanField(default=False)
    it_park = models.BooleanField(default=False)
    omborchi = models.BooleanField(default=False)
    prorektor_izoh = models.CharField(max_length=255, blank=True)
    bugalter_izoh = models.CharField(max_length=255, blank=True)
    xojalik_bolimi_izoh = models.CharField(max_length=255, blank=True)
    it_park_izoh = models.CharField(max_length=255, blank=True)
    omborchi_izoh = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return self.user.username   

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
    
class RadEtilganMaxsulotlar(AsosiyModel):
    buyurtma = models.ForeignKey(Buyurtma, on_delete=models.CASCADE)
    maxsulot = models.ForeignKey(Maxsulot, on_delete=models.CASCADE)
    qiymat = models.DecimalField(max_digits=10, decimal_places=2) 
    birlik = models.ForeignKey(Birlik, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.maxsulot.name
    
class Talabnoma(AsosiyModel):
    buyurtma = models.ForeignKey(Buyurtma, on_delete=models.CASCADE)
    talabnoma_pdf = models.FileField(upload_to='talabnoma_pdf')
    talabnoma_pdf_link = models.CharField(max_length=255)

    def __str__(self):
        return self.buyurtma
