import os, io
import base64
import qrcode
from io import BytesIO
import datetime as dt
from django.core.files.base import ContentFile
from django.template.loader import get_template
from asosiy.settings import DOMEN
from xhtml2pdf import pisa
from django.db import models
from decimal import Decimal
from users.choices import UserRoleChoice, MaxsulotRoleChoice
from users.models import AsosiyModel, Users


class Kategoriya(AsosiyModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Birlik(AsosiyModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Maxsulot(AsosiyModel):
    kategoriya = models.ForeignKey(Kategoriya, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    maxsulot_role = models.CharField(max_length=30, choices=MaxsulotRoleChoice.choices, default=MaxsulotRoleChoice.XOJALIK)
    birlik = models.ForeignKey(Birlik, on_delete=models.CASCADE)
    maxviylik = models.BooleanField(default=False)
    rasm = models.ImageField(upload_to='maxsulot', null=True)
    
    def __str__(self):
        return self.name


class OmborniYopish(AsosiyModel):
    yopish = models.BooleanField(default=False)

    def __str__(self):
        return self.yopish

class Ombor(AsosiyModel):
    maxsulot = models.ForeignKey(Maxsulot, on_delete=models.CASCADE)
    qiymat = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return self.maxsulot.name 
    
class JamiMahsulot(AsosiyModel):
    maxsulot = models.ForeignKey(Maxsulot, on_delete=models.CASCADE)
    qiymat = models.DecimalField(max_digits=10, decimal_places=1, default=Decimal('0.00')) 

    def __str__(self):
        return self.maxsulot.name 


# buyurtma

class Buyurtma(AsosiyModel):
    komendant_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    buyurtma_role = models.CharField(max_length=30, choices=UserRoleChoice.choices)
    tasdiqlash = models.BooleanField(default=False)
    rad_etish = models.BooleanField(default=False)
    izoh = models.CharField(max_length=355, blank=True)

    def __str__(self):
        return self.user.username   
    
class BuyurtmaMaxsulot(AsosiyModel):
    buyurtma = models.ForeignKey(Buyurtma, on_delete=models.CASCADE)
    maxsulot = models.ForeignKey(Maxsulot, on_delete=models.CASCADE)
    qiymat = models.DecimalField(max_digits=10, decimal_places=2)   

    def __str__(self):
        return self.user.username   

# korzinka

class Korzinka(AsosiyModel):
    komendant_user = models.OneToOneField(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class KorzinkaMaxsulot(AsosiyModel):
    korzinka = models.ForeignKey(Korzinka, on_delete=models.CASCADE)
    maxsulot = models.ForeignKey(Maxsulot, on_delete=models.CASCADE)
    qiymat = models.DecimalField(max_digits=10, decimal_places=2) 
    sorov = models.BooleanField(default=False)

    def __str__(self):
        return self.maxsulot.name


class OlinganMaxsulotlar(AsosiyModel):
    buyurtma = models.ForeignKey(Buyurtma, on_delete=models.CASCADE)
    maxsulot = models.ForeignKey(Maxsulot, on_delete=models.CASCADE)
    qiymat = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.maxsulot.name
    
class RadEtilganMaxsulotlar(AsosiyModel):
    rad_etgan_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    buyurtma = models.ForeignKey(Buyurtma, on_delete=models.CASCADE)
    maxsulot = models.ForeignKey(Maxsulot, on_delete=models.CASCADE)
    qiymat = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.maxsulot.name
    
class Talabnoma(models.Model):
    buyurtma = models.ForeignKey('Buyurtma', on_delete=models.CASCADE)
    talabnoma_pdf = models.FileField(upload_to='talabnoma_pdf', null=True, blank=True)

    def __str__(self):
        return str(self.buyurtma)

    def pdf_create(self):
        # Buyurtma obyektini olish
        buyurtma = self.buyurtma

        # Template yo‘lini ko‘rsatish
        template_path = 'talabnoma.html'

        # malumotlarni chaqirish
        maxsulotlar = OlinganMaxsulotlar.objects.filter(buyurtma=buyurtma)
        prorektor = Users.objects.filter(role=UserRoleChoice.PROREKTOR).first()
        bugalter = Users.objects.filter(role=UserRoleChoice.BUGALTER).first()
        xojalik = Users.objects.filter(role=UserRoleChoice.XOJALIK).first()
        rttm = Users.objects.filter(role=UserRoleChoice.RTTM).first()
        omborchi = Users.objects.filter(role=UserRoleChoice.OMBORCHI).first()
        komendant = f'{buyurtma.user.last_name} {buyurtma.user.first_name}'
        bino = f'{buyurtma.user.bino}'
        sana = buyurtma.created_at

        # QR Kod yaratish
        data = f"https://ombor.kspi.uz/talabnoma/{buyurtma.id}/"
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(data)
        qr.make()
        img = qr.make_image()

        # QR Kodni Base64 formatiga o‘tkazish
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()

        # Kontekstni tayyorlash
        context = {
            'maxsulotlar': maxsulotlar,
            'prorektor': prorektor,
            'bugalter': bugalter,
            'xojalik': xojalik,
            'rttm': rttm,
            'omborchi': omborchi,
            'komendant': komendant,
            'bino': bino,
            'sana': sana,
            'qr_code': qr_base64,  
        }

        # Template-ni yuklab, HTML hosil qilish
        template = get_template(template_path)
        html = template.render(context)

        # PDFni vaqtinchalik xotirada yaratish
        pdf_buffer = io.BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)

        if not pisa_status.err:
            # Fayl nomini yaratish
            pdf_name = f"talabnoma_{self.buyurtma.id}_{sana.strftime('%Y%m%d%H%M%S')}.pdf"
            
            # Faylni saqlash uchun FileField-dan foydalanish
            self.talabnoma_pdf.save(pdf_name, ContentFile(pdf_buffer.getvalue()), save=False)
            pdf_buffer.close()
            self.save()
            return True  # Muvaffaqiyatli saqlandi
        else:
            pdf_buffer.close()
            return False  # Xatolik yuz berdi

    def save(self, *args, **kwargs):
        # Obyektni avval saqlab, so‘ngra PDFni yaratish
        super().save(*args, **kwargs)
        if not self.talabnoma_pdf:  # Agar PDF hali yaratilmagan bo‘lsa
            self.pdf_create()