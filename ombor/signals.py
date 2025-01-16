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

    if korzinka_mahsulotlari.exists():
        for mahsulot in korzinka_mahsulotlari:
            maxsulot_role = mahsulot.maxsulot.maxsulot_role

            # Foydalanuvchiga mos aktiv buyurtmani topish yoki yaratish
            buyurtma, created = Buyurtma.objects.get_or_create(
                komendant_user=komendant_user,
                maxsulot_role=maxsulot_role,  # Mahsulot roli asosida
                active=True,
                defaults={
                    "buyurtma_role": maxsulot_role,
                    "prorektor": False,
                    "bugalter": False,
                    "omborchi": False,
                    "rttm": False,
                    "xojalik": False,
                    "sorov": False,
                    "tasdiqlash": False,
                    "rad_etish": False,
                    "izoh": " ",
                }
            )

            # Mahsulotni buyurtmaga qo‘shish
            BuyurtmaMaxsulot.objects.get_or_create(
                buyurtma=buyurtma,
                maxsulot=mahsulot.maxsulot,
                defaults={"qiymat": mahsulot.qiymat}
            )


@receiver(post_save, sender=KorzinkaMaxsulot)
def add_korzinka_maxsulot(sender, instance, created, **kwargs):
    """
    Mahsulot roliga qarab mos korzinkaga mahsulotni qo'shish.
    """
    if created:  # Faqat yangi yozuv yaratilganda ishlaydi
        maxsulot = instance.maxsulot
        user = instance.korzinka.komendant_user

        # Foydalanuvchining mahsulot roliga mos keladigan korzinkasini topish
        korzinka, created = Korzinka.objects.get_or_create(
            komendant_user=user,
            maxsulot_role=maxsulot.maxsulot_role,  # Maxsulot roli asosida korzinka
        )

        # Korzinkaga mahsulotni qo'shish
        if not KorzinkaMaxsulot.objects.filter(korzinka=korzinka, maxsulot=maxsulot).exists():
            KorzinkaMaxsulot.objects.create(
                korzinka=korzinka,
                maxsulot=maxsulot,
                qiymat=instance.qiymat,
            )



@receiver(post_save, sender=Buyurtma)
def update_buyurtma_post_save(sender, instance, created, **kwargs):
    """
    Buyurtma yaratilganidan yoki yangilanganidan keyin avtomatik bog'liq o'zgarishlarni qo'llash.
    """

    if created:
        print(f"Yangi buyurtma yaratildi: {instance.komendant_user.username} uchun")
    else:
        print(f"Buyurtma yangilandi: {instance.komendant_user.username} uchun")

    # Bog'liq mahsulotlarni avtomatik yangilash
    buyurtma_mahsulotlari = BuyurtmaMaxsulot.objects.filter(buyurtma=instance)
    if buyurtma_mahsulotlari.exists():
        for mahsulot in buyurtma_mahsulotlari:
            if mahsulot.qiymat <= 0:
                mahsulot.delete() 

