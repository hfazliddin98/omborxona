import os, io
import base64
import qrcode
from io import BytesIO
import datetime as dt
from django.core.files.base import ContentFile
from django.template.loader import get_template
from asosiy.settings import DOMEN
from xhtml2pdf import pisa
from django.conf import settings
from django.db import models
from decimal import Decimal
from users.choices import UserRoleChoice, MaxsulotRoleChoice
from users.models import AsosiyModel, Users
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import qrcode
from io import BytesIO
import os
from django.contrib.staticfiles import finders 
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader


class Kategoriya(AsosiyModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Birlik(AsosiyModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Maxsulot(AsosiyModel):
    kategoriya = models.ForeignKey(Kategoriya, related_name='maxsulot', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    maxsulot_role = models.CharField(max_length=30, choices=MaxsulotRoleChoice.choices, default=MaxsulotRoleChoice.XOJALIK)
    birlik = models.ForeignKey(Birlik, on_delete=models.CASCADE)
    maxviylik = models.BooleanField(default=False)
    rasm = models.ImageField(upload_to='maxsulot', null=True)
    
    def __str__(self):
        return self.name

  

class OmborniYopish(AsosiyModel):
    yopish = models.BooleanField(default=False)


class Ombor(AsosiyModel):
    maxsulot = models.ForeignKey(Maxsulot, on_delete=models.CASCADE)
    qiymat = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return self.maxsulot.name 
    

class JamiMahsulot(AsosiyModel):
    maxsulot = models.OneToOneField(Maxsulot, on_delete=models.CASCADE)
    qiymat = models.DecimalField(max_digits=10, decimal_places=1, default=Decimal('0.00')) 

    def __str__(self):
        return self.maxsulot.name 



# korzinka

class Korzinka(AsosiyModel):
    komendant_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    maxsulot_role = models.CharField(max_length=30, choices=MaxsulotRoleChoice.choices)

    def __str__(self):
        return self.komendant_user.username
    
class KorzinkaMaxsulot(AsosiyModel):
    korzinka = models.ForeignKey(Korzinka, on_delete=models.CASCADE, related_name='maxsulotlar')
    maxsulot = models.ForeignKey(Maxsulot, on_delete=models.CASCADE)
    qiymat = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return self.maxsulot.name
    
# buyurtma

class Buyurtma(AsosiyModel):
    komendant_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    maxsulot_role = models.CharField(max_length=30, choices=MaxsulotRoleChoice.choices)
    buyurtma_role = models.CharField(max_length=30, choices=UserRoleChoice.choices)
    prorektor = models.BooleanField(default=False)
    bugalter = models.BooleanField(default=False)
    omborchi = models.BooleanField(default=False)
    rttm = models.BooleanField(default=False)
    xojalik = models.BooleanField(default=False)
    active  = models.BooleanField(default=False)
    tasdiqlash = models.BooleanField(default=False)
    rad_etish = models.BooleanField(default=False)
    izoh = models.CharField(max_length=355, blank=True)

    def __str__(self):
        return self.komendant_user.username
    
class BuyurtmaMaxsulot(AsosiyModel):
    buyurtma = models.ForeignKey(Buyurtma, on_delete=models.CASCADE, related_name='maxsulotlar')
    maxsulot = models.ForeignKey(Maxsulot, on_delete=models.CASCADE)
    qiymat = models.DecimalField(max_digits=10, decimal_places=2)   

    def __str__(self):
        return self.maxsulot.name 

class OlinganMaxsulot(AsosiyModel):
    buyurtma = models.ForeignKey(Buyurtma, on_delete=models.CASCADE, related_name='olingan_maxsulotlar')
    maxsulot = models.ForeignKey(Maxsulot, on_delete=models.CASCADE)
    qiymat = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.buyurtma} - {self.maxsulot.name}"
 

    
class RadEtilganMaxsulot(AsosiyModel):
    rad_etgan_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    buyurtma = models.ForeignKey(Buyurtma, on_delete=models.CASCADE)
    active  = models.BooleanField(default=True)
   
    def __str__(self):
        return f"{self.buyurtma} raqamli buyurtma"




def generate_qr_code_base64(buyurtma_id):
    """
    QR kodni yaratib, Base64 formatida qaytarish.
    :param buyurtma_id: Buyurtma identifikatori.
    :return: QR kodning Base64 formatidagi qiymati.
    """
    # QR Kod yaratish
    data = f"https://ombor.kspi.uz/talabnoma/{buyurtma_id}/"
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make()
    img = qr.make_image(fill='black', back_color='white')

    # QR Kodni Base64 formatiga o‘tkazish
    buffer = BytesIO()
    img.save(buffer, format="PNG")  # QR-kodni PNG formatida saqlash
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')  # Base64 formatiga o'tkazish
    buffer.close()

    return qr_base64

def generate_pdf_rus(file_path, data):
    """
    Rus alifbosi asosida PDF yaratish.
    :param file_path: Saqlanadigan PDF fayl yo'li.
    :param data: Talabnoma uchun ma'lumotlar (sarlavha, jadval, QR kod).
    """
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4


    # Static katalogdagi shrift faylini yuklash
    font_path = os.path.join(settings.STATIC_ROOT, 'font', 'FreeSerif.ttf')

    pdfmetrics.registerFont(TTFont('FreeSerif', font_path))
    c.setFont("FreeSerif", 12)

    # 1. Sarlavha va asosiy ma'lumotlar
    current_height = height - 50  # Dinamik joylashuv boshqaruvi
    c.drawString(350, current_height, "Қўқон Давлат Педагогика Институти")
    current_height -= 20
    c.drawString(350, current_height, "Молия ва иқтисодиёт ишлари бўйича")
    current_height -= 20
    c.drawString(350, current_height, data['prorektor_nomi'])
    current_height -= 20
    c.drawString(350, current_height, data['bino'])
    current_height -= 20
    c.drawString(350, current_height, data['komandant_nomi'])

    # 2. Sana va talabnoma matni
    current_height -= 40
    c.setFont("FreeSerif", 14)
    c.drawString(250, current_height, "ТАЛАБНОМА")
    current_height -= 40
    c.setFont("FreeSerif", 12)
    c.drawString(60, current_height, data['sana'])
    current_height -= 30
    c.drawString(60, current_height, data['matn'])

    # Jadval ustunlarining kengligi
    column_widths = [30, 370, 80]  # №, Mahsulot, Qiymat

    # Jadval boshidan boshlash
    c.setFont("FreeSerif", 12)
    current_height -= 40
    x_position = 60  # Jadvalning boshlanish x koordinatasi
    row_height = 20  # Har bir qator balandligi

    # Boshqa rangda ustun nomlarini chizish (masalan, sarlavhalar)
    c.setFillColorRGB(0.8, 0.8, 0.8)  # Sarlavhalar uchun to‘ldirish rangini o‘zgartirish
    c.rect(x_position, current_height, sum(column_widths), row_height, stroke=1, fill=1)

    # Sarlavha matnini chizish
    c.setFillColorRGB(0, 0, 0)  # Sarlavhalar qora rangda bo‘lishi uchun
    c.drawString(x_position + 5, current_height + 5, "№")
    c.drawString(x_position + column_widths[0] + 5, current_height + 5, "Маҳсулот")
    c.drawString(x_position + column_widths[0] + column_widths[1] + 5, current_height + 5, "Қиймат")

    # Sarlavha oxirida balandlikni yangilash
    current_height -= row_height

    # Har bir mahsulot uchun qatorlarni chizish
    for idx, mahsulot in enumerate(data['maxsulotlar'], start=1):

        # QR kod va boshqa ma'lumotlarni chizish
        if current_height <= 100:  # Agar sahifa tugashga yaqin bo'lsa
            c.showPage()  # Yangi sahifa ochish
            font_path = os.path.join(settings.STATIC_ROOT, 'font', 'FreeSerif.ttf')
            pdfmetrics.registerFont(TTFont('FreeSerif', font_path))
            c.setFont("FreeSerif", 12)
            current_height = height - 50  # Yangi sahifadagi boshlang'ich balandlik

        # Har bir qatorni chizish
        c.rect(x_position, current_height, sum(column_widths), row_height, stroke=1, fill=0)

        # Ma'lumotlarni joylashtirish
        c.drawString(x_position + 5, current_height + 5, f"{idx}")
        c.drawString(x_position + column_widths[0] + 5, current_height + 5, f"{mahsulot.maxsulot}")
        c.drawString(x_position + column_widths[0] + column_widths[1] + 5, current_height + 5, f"{mahsulot.qiymat} {mahsulot.maxsulot.birlik}")

        # Qator balandligini yangilash
        current_height -= row_height







    

     # QR kod va boshqa ma'lumotlarni chizish
    if current_height <= 100:  # Agar sahifa tugashga yaqin bo'lsa
        c.showPage()  # Yangi sahifa ochish
        font_path = os.path.join(settings.STATIC_ROOT, 'font', 'FreeSerif.ttf')
        pdfmetrics.registerFont(TTFont('FreeSerif', font_path))
        c.setFont("FreeSerif", 12)
        current_height = height - 50  # Yangi sahifadagi boshlang'ich balandlik


    current_height -= 40
    c.drawString(60, current_height, "Молия ва иқтисодиёт ишлари бўйича проректори :")
    current_height -= 30
    if data['prorektor'].qr_code_link:  # QR-kod mavjudligini tekshirish
        qr_path = data['prorektor'].qr_code_link  # Rasm url
        qr_image = ImageReader(qr_path)
        c.drawString(60, current_height+15, data['prorektor_fish'])
        c.drawImage(qr_image, 500, current_height, width=50, height=50)
    else:
        c.drawString(450, current_height, "QR-код мавжуд эмас.")



    if current_height <= 100:  # Agar sahifa tugashga yaqin bo'lsa
        c.showPage()  # Yangi sahifa ochish

        # Static katalogdagi shrift faylini yuklash
        font_path = os.path.join(settings.STATIC_ROOT, 'font', 'FreeSerif.ttf')

        pdfmetrics.registerFont(TTFont('FreeSerif', font_path))
        c.setFont("FreeSerif", 12)
        current_height = height - 50  # Yangi sahifadagi boshlang'ich balandlik

    current_height -= 20
    c.drawString(60, current_height, "Бугалтер :")
    current_height -= 30
    if data['bugalter'].qr_code_link:  # QR-kod mavjudligini tekshirish
        qr_path = data['bugalter'].qr_code_link  # Rasm url
        qr_image = ImageReader(qr_path)
        c.drawString(60, current_height+15, data['bugalter_fish'])
        c.drawImage(qr_image, 500, current_height, width=50, height=50)
    else:
        c.drawString(450, current_height, "QR-код мавжуд эмас.")



    if current_height <= 100:  # Agar sahifa tugashga yaqin bo'lsa
        c.showPage()  # Yangi sahifa ochish

        # Static katalogdagi shrift faylini yuklash
        font_path = os.path.join(settings.STATIC_ROOT, 'font', 'FreeSerif.ttf')

        pdfmetrics.registerFont(TTFont('FreeSerif', font_path))
        c.setFont("FreeSerif", 12)
        current_height = height - 50  # Yangi sahifadagi boshlang'ich balandlik

    current_height -= 20
    c.drawString(60, current_height, "Омборчи :")
    current_height -= 30
    if data['omborchi'].qr_code_link:  # QR-kod mavjudligini tekshirish
        qr_path = data['omborchi'].qr_code_link  # Rasm url
        qr_image = ImageReader(qr_path)
        c.drawString(60, current_height+15, data['omborchi_fish'])
        c.drawImage(qr_image, 500, current_height, width=50, height=50)
    else:
        c.drawString(450, current_height, "QR-код мавжуд эмас.")



    if current_height <= 100:  # Agar sahifa tugashga yaqin bo'lsa
        c.showPage()  # Yangi sahifa ochish

        # Static katalogdagi shrift faylini yuklash
        font_path = os.path.join(settings.STATIC_ROOT, 'font', 'FreeSerif.ttf')

        pdfmetrics.registerFont(TTFont('FreeSerif', font_path))
        c.setFont("FreeSerif", 12)
        current_height = height - 50  # Yangi sahifadagi boshlang'ich balandlik

    current_height -= 20
    c.drawString(60, current_height, "РТТМ :")
    current_height -= 30
    if data['rttm'].qr_code_link:  # QR-kod mavjudligini tekshirish
        qr_path = data['rttm'].qr_code_link  # Rasm url
        qr_image = ImageReader(qr_path)
        c.drawString(60, current_height+15, data['rttm_fish'])
        c.drawImage(qr_image, 500, current_height, width=50, height=50)
    else:
        c.drawString(450, current_height, "QR-код мавжуд эмас.")




    if current_height <= 100:  # Agar sahifa tugashga yaqin bo'lsa
        c.showPage()  # Yangi sahifa ochish

        # Static katalogdagi shrift faylini yuklash
        font_path = os.path.join(settings.STATIC_ROOT, 'font', 'FreeSerif.ttf')

        pdfmetrics.registerFont(TTFont('FreeSerif', font_path))
        c.setFont("FreeSerif", 12)
        current_height = height - 50  # Yangi sahifadagi boshlang'ich balandlik

    current_height -= 20
    c.drawString(60, current_height, "Хўжалик бўлими :")
    current_height -= 30
    if data['xojalik'].qr_code_link:  # QR-kod mavjudligini tekshirish
        qr_path = data['xojalik'].qr_code_link  # Rasm url
        qr_image = ImageReader(qr_path)
        c.drawString(60, current_height+15, data['xojalik_fish'])
        c.drawImage(qr_image, 500, current_height, width=50, height=50)
    else:
        c.drawString(450, current_height, "QR-код мавжуд эмас.")




    if current_height <= 100:  # Agar sahifa tugashga yaqin bo'lsa
        c.showPage()  # Yangi sahifa ochish

        # Static katalogdagi shrift faylini yuklash
        font_path = os.path.join(settings.STATIC_ROOT, 'font', 'FreeSerif.ttf')

        pdfmetrics.registerFont(TTFont('FreeSerif', font_path))
        c.setFont("FreeSerif", 12)
        current_height = height - 50  # Yangi sahifadagi boshlang'ich balandlik

    current_height -= 150
    if data['buyurtma']:
        print(data['buyurtma'])
        qr_base64 = generate_qr_code_base64(data['buyurtma'])  # QR kodni base64 formatida olish
        buffer = BytesIO(base64.b64decode(qr_base64))  # Base64'dan rasmga o'tkazish
        qr_image = ImageReader(buffer)
        c.drawImage(qr_image, 60, current_height, width=100, height=100)
    else:
        c.drawString(450, current_height, "QR-код мавжуд эмас.")
  
    # PDFni saqlash
    c.save()


class Talabnoma(AsosiyModel):
    buyurtma = models.ForeignKey('Buyurtma', on_delete=models.CASCADE)
    talabnoma_pdf = models.FileField(upload_to='talabnoma_pdf', null=True, blank=True)
    active = models.BooleanField(default=True)

    def pdf_create(self):
        # Ma'lumotlarni yig'ish
        buyurtma = self.buyurtma
        maxsulotlar = BuyurtmaMaxsulot.objects.filter(buyurtma=buyurtma)
        prorektor = Users.objects.filter(role=UserRoleChoice.PROREKTOR).first()
        bugalter = Users.objects.filter(role=UserRoleChoice.BUGALTER).first()
        xojalik = Users.objects.filter(role=UserRoleChoice.XOJALIK).first()
        rttm = Users.objects.filter(role=UserRoleChoice.RTTM).first()
        omborchi = Users.objects.filter(role=UserRoleChoice.OMBORCHI).first()
        komendant = f'{buyurtma.komendant_user.last_name} {buyurtma.komendant_user.first_name}'
        bino = f'{buyurtma.komendant_user.bino}'
        data = {
            'prorektor_nomi': f"проректори {prorektor.last_name} {prorektor.first_name}га",
            'bino': f"{bino} коменданти",
            'komandant_nomi': f"{komendant}дан",
            'sana': f"{buyurtma.created_at}",
            'matn': f"Менга институт омборидан {bino} учун қуйидагиларни беришингизни сўрайман.",
            'maxsulotlar': maxsulotlar,
            'prorektor': prorektor,
            'prorektor_fish': f"{prorektor.last_name} {prorektor.first_name}",
            'bugalter': bugalter,
            'bugalter_fish': f"{bugalter.last_name} {bugalter.first_name}",
            'omborchi': omborchi,
            'omborchi_fish': f"{omborchi.last_name} {omborchi.first_name}",
            'rttm': rttm,
            'rttm_fish': f"{rttm.last_name} {rttm.first_name}",
            'xojalik': xojalik,
            'xojalik_fish': f"{xojalik.last_name} {xojalik.first_name}",
            'buyurtma': buyurtma.id,
        }

        # Fayl nomini yaratish
        file_path = f"media/talabnoma_pdf/talabnoma_{buyurtma.id}.pdf"

        # PDF yaratish
        generate_pdf_rus(file_path, data)

        # PDFni FileField-ga saqlash
        with open(file_path, 'rb') as pdf_file:
            self.talabnoma_pdf.save(os.path.basename(file_path), ContentFile(pdf_file.read()), save=False)
        self.save()

    def save(self, *args, **kwargs):
        # Obyektni avval saqlab, keyin PDFni yaratish
        super().save(*args, **kwargs)
        if not self.talabnoma_pdf:  # Agar PDF yaratilmagan bo'lsa
            self.pdf_create()
