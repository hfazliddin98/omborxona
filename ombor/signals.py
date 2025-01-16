from django.db.models.signals import post_save, post_delete, pre_delete
from django.db.models import Sum
from django.dispatch import receiver
from decimal import Decimal
from .models import Ombor, JamiMahsulot, OlinganMaxsulot
from .models import Korzinka, KorzinkaMaxsulot, Buyurtma, BuyurtmaMaxsulot
from users.choices import MaxsulotRoleChoice


@receiver(post_save, sender=Ombor)
def update_jami_mahsulot_on_save(sender, instance, created, **kwargs):
    # JamiMahsulot obyektini olish yoki yaratish
    jami_mahsulot, _ = JamiMahsulot.objects.get_or_create(maxsulot=instance.maxsulot)
    
    # Ombordagi mahsulot qiymatini hisoblash
    jami_qiymat = Ombor.objects.filter(maxsulot=instance.maxsulot).aggregate(
        total_qiymat=Sum('qiymat')
    )['total_qiymat'] or Decimal('0.00')
    
    # OlinganMaxsulot qiymatini hisoblash
    olingan_qiymat = OlinganMaxsulot.objects.filter(maxsulot=instance.maxsulot).aggregate(
        total_qiymat=Sum('qiymat')
    )['total_qiymat'] or Decimal('0.00')

    # JamiMahsulot qiymatini yangilash
    jami_mahsulot.qiymat = jami_qiymat - olingan_qiymat
    jami_mahsulot.save()

@receiver(post_delete, sender=Ombor)
def update_jami_mahsulot_on_delete(sender, instance, **kwargs):
    # JamiMahsulot obyektini olish yoki yaratish
    jami_mahsulot, _ = JamiMahsulot.objects.get_or_create(maxsulot=instance.maxsulot)
    
    # Ombordagi mahsulot qiymatini hisoblash
    jami_qiymat = Ombor.objects.filter(maxsulot=instance.maxsulot).aggregate(
        total_qiymat=Sum('qiymat')
    )['total_qiymat'] or Decimal('0.00')
    
    # OlinganMaxsulot qiymatini hisoblash
    olingan_qiymat = OlinganMaxsulot.objects.filter(maxsulot=instance.maxsulot).aggregate(
        total_qiymat=Sum('qiymat')
    )['total_qiymat'] or Decimal('0.00')

    # JamiMahsulot qiymatini yangilash
    jami_mahsulot.qiymat = jami_qiymat - olingan_qiymat
    jami_mahsulot.save()

@receiver(post_save, sender=OlinganMaxsulot)
@receiver(post_delete, sender=OlinganMaxsulot)
def update_jami_mahsulot_on_olingan(sender, instance, **kwargs):
    # JamiMahsulot obyektini olish yoki yaratish
    jami_mahsulot, _ = JamiMahsulot.objects.get_or_create(maxsulot=instance.maxsulot)

    # Ombordagi mahsulot qiymatini hisoblash
    jami_qiymat = Ombor.objects.filter(maxsulot=instance.maxsulot).aggregate(
        total_qiymat=Sum('qiymat')
    )['total_qiymat'] or Decimal('0.00')
    
    # OlinganMaxsulot qiymatini hisoblash
    olingan_qiymat = OlinganMaxsulot.objects.filter(maxsulot=instance.maxsulot).aggregate(
        total_qiymat=Sum('qiymat')
    )['total_qiymat'] or Decimal('0.00')

    # JamiMahsulot qiymatini yangilash
    jami_mahsulot.qiymat = jami_qiymat - olingan_qiymat
    jami_mahsulot.save()



@receiver(pre_delete, sender=Korzinka)
def add_to_buyurtma_on_korzinka_delete(sender, instance, **kwargs):
    komendant_user = instance.komendant_user
    korzinka_mahsulotlari = KorzinkaMaxsulot.objects.filter(korzinka=instance)

    # Mahsulotlarni maxsulot_role bo'yicha ajratish
    mahsulotlar_by_role = {
        MaxsulotRoleChoice.XOJALIK: [],
        MaxsulotRoleChoice.RTTM: []
    }

    for mahsulot in korzinka_mahsulotlari:
        if mahsulot.maxsulot.maxsulot_role == MaxsulotRoleChoice.XOJALIK:
            mahsulotlar_by_role[MaxsulotRoleChoice.XOJALIK].append(mahsulot)
        elif mahsulot.maxsulot.maxsulot_role == MaxsulotRoleChoice.RTTM:
            mahsulotlar_by_role[MaxsulotRoleChoice.RTTM].append(mahsulot)

    # Har bir mahsulot turi uchun alohida buyurtmalar yaratish yoki qo'shish
    for role, mahsulotlar in mahsulotlar_by_role.items():
        if mahsulotlar:
            # Shu mahsulot turi uchun mavjud buyurtmani tekshirish
            buyurtma = Buyurtma.objects.filter(
                komendant_user=komendant_user,
                buyurtma_role=role,
                active=True,
                sorov=False,
                tasdiqlash=False
            ).first()

            if not buyurtma:
                # Yangi buyurtma yaratish
                buyurtma = Buyurtma.objects.create(
                    komendant_user=komendant_user,
                    buyurtma_role=role,
                    active=True,
                    sorov=False,
                    tasdiqlash=False,
                    rad_etish=False,
                    izoh=f"{role} mahsulotlar uchun avtomatik yaratildi"
                )

            # Mahsulotlarni shu buyurtmaga qo'shish
            for mahsulot in mahsulotlar:
                BuyurtmaMaxsulot.objects.create(
                    buyurtma=buyurtma,
                    maxsulot=mahsulot.maxsulot,
                    qiymat=mahsulot.qiymat
                )

      



# @receiver(pre_delete, sender=Korzinka)
# def add_to_buyurtma_on_korzinka_delete(sender, instance, **kwargs):
#     komendant_user = instance.komendant_user
#     # Buyurtma tekshiruvi
#     buyurtma = Buyurtma.objects.filter(
#         komendant_user=komendant_user, 
#         active=False, 
#         sorov=False
#     ).first()

#     if not buyurtma:
#         # Yangi buyurtma yaratish agar mavjud bo'lmasa
#         buyurtma = Buyurtma.objects.create(
#             komendant_user=komendant_user,
#             buyurtma_role='standart',  # Kerakli rolni sozlang
#             active=False,
#             sorov=False,
#             tasdiqlash=False,
#             rad_etish=False,
#             izoh="Korzinka o'chirilishi vaqtida avtomatik yaratildi"
#         )

#     # Korzinkaga bog'liq barcha mahsulotlarni olish
#     korzinka_mahsulotlari = KorzinkaMaxsulot.objects.filter(korzinka=instance)

#     # Har bir mahsulotni BuyurtmaMaxsulotga qo'shish
#     for mahsulot in korzinka_mahsulotlari:
#         BuyurtmaMaxsulot.objects.create(
#             buyurtma=buyurtma,
#             maxsulot=mahsulot.maxsulot,
#             qiymat=mahsulot.qiymat
#         )




