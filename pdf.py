from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import qrcode
from io import BytesIO
import os
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Hujjatni yaratish
def create_pdf(file_name):
    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4

    # Shriftni qo'shish
    pdfmetrics.registerFont(TTFont('FreeSerif', '/Users/fazliddin/github/omborxona/static/font/FreeSerif.ttf'))  # FreeSerif.ttf faylini to'g'ri yo'lda saqlang
    c.setFont("FreeSerif", 12)

    # 1. Sarlavha va asosiy ma'lumotlar
    sarlavha = "Кокандский государственный педагогический институт"
    prorektor = "Проректор по финансам и экономике"
    komandant = "Командант 1-XXXXXX"
    sana = "21 Января, 2025 год"

    c.drawString(300, height - 50, sarlavha)
    c.setFont("FreeSerif", 10)
    c.drawString(300, height - 70, prorektor)
    c.drawString(300, height - 90, komandant)
    c.drawString(300, height - 110, sana)

    # 2. Sana va talabnoma matni
    c.drawString(50, height - 150, sana)
    c.setFont("FreeSerif", 12)
    c.drawString(250, height - 170, "Заявление")
    c.setFont("FreeSerif", 10)
    talabnoma_matini = "Прошу вас предоставить мне следующие материалы из института:"
    c.drawString(50, height - 200, talabnoma_matini)

    # 3. Jadval
    data = [["№", "Наименование товара", "Количество"],
            ["1", "Бумага для документов", "20,00 штук"],
            ["2", "Ручки", "15,00 штук"]]

    table = Table(data, colWidths=[50, 300, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'FreeSerif'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    table.wrapOn(c, width, height)
    table.drawOn(c, 50, height - 300)

    # 4. QR-kodlar qo'shish
    qr_data_list = [
        "Проректор по финансам и экономике:",
        "Бухгалтер:",
        "Хозяйственный отдел:"
    ]
    x_position = 50
    y_position = height - 500

    for data in qr_data_list:
        qr = qrcode.QRCode(box_size=5, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # QR-kodni PDFga qo'shish
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)  # BytesIO obyektini boshlanishiga qaytarish

        # Vaqtinchalik faylga saqlash
        qr_image_path = "temp_qr_image.png"
        with open(qr_image_path, "wb") as f:
            f.write(buffer.getvalue())

        # QR-kodni PDFga qo'shish
        c.drawImage(qr_image_path, x_position, y_position, 50, 50)
        c.drawString(x_position + 60, y_position + 20, data)
        y_position -= 70

        # Vaqtinchalik faylni o'chirish
        os.remove(qr_image_path)

    # Hujjatni saqlash
    c.save()

# PDF yaratish
create_pdf("zayavlenie_rus_with_font.pdf")
