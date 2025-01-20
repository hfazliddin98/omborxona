import requests
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.db.models import Sum
from django.dispatch import receiver
from decimal import Decimal
from .models import Ombor, JamiMahsulot, OlinganMaxsulot, RadEtilganMaxsulot
from .models import Korzinka, KorzinkaMaxsulot, Buyurtma, BuyurtmaMaxsulot, Talabnoma
from users.choices import MaxsulotRoleChoice, UserRoleChoice
from users.middleware import get_current_request




@receiver(pre_delete, sender=Korzinka)
def add_to_buyurtma_on_korzinka_delete(sender, instance, **kwargs):
    komendant_user = instance.komendant_user
    korzinka_mahsulotlari = KorzinkaMaxsulot.objects.filter(korzinka=instance)

    if korzinka_mahsulotlari.exists():
        for mahsulot in korzinka_mahsulotlari:
            maxsulot_role = mahsulot.maxsulot.maxsulot_role  # Mahsulotning roli

            # Foydalanuvchiga mos aktiv buyurtmani topish yoki yaratish
            buyurtma, created = Buyurtma.objects.get_or_create(
                komendant_user=komendant_user,
                maxsulot_role=maxsulot_role,  # Mahsulot roli asosida
                active=True,
                defaults={
                    "buyurtma_role": mahsulot.maxsulot.maxsulot_role,  # Komendant roli asosida buyurtma roli
                    "prorektor": False,
                    "bugalter": False,
                    "omborchi": False,
                    "rttm": False,
                    "xojalik": False,
                    "tasdiqlash": False,
                    "rad_etish": False,
                    "izoh": f"Avtomatik yaratildi: {maxsulot_role}",
                }
            )

            # Mahsulotni buyurtmaga qo‘shish (agar mavjud bo'lmasa)
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



@receiver(pre_save, sender=Buyurtma)
def update_buyurtma_pre_save(sender, instance, **kwargs):
    """
    Buyurtma yaratilganda yoki yangilanganida avtomatik qiymatlarni o'zgartirish.
    """
    # Faqat mavjud bo'lgan obyektni yangilashda ishlaydi
    if instance.pk:  # Obyekt allaqachon mavjud bo'lsa (yangilash jarayoni)
        if instance.rttm or instance.xojalik:
            instance.buyurtma_role = UserRoleChoice.PROREKTOR
        if instance.prorektor:
            instance.buyurtma_role = UserRoleChoice.BUGALTER
        if instance.bugalter:
            instance.buyurtma_role = UserRoleChoice.OMBORCHI
        if instance.omborchi:
            instance.active = False
            instance.tasdiqlash = True


            if not Talabnoma.objects.filter(buyurtma=instance).exists():
                Talabnoma.objects.create(buyurtma=instance)

            # Buyurtma bilan bog‘liq barcha mahsulotlarni olish
            buyurtma_maxsulotlar = BuyurtmaMaxsulot.objects.filter(buyurtma=instance)

           
            for buyurtma_maxsulot in buyurtma_maxsulotlar:
                # Agar OlinganMaxsulot bo'lmasa, yaratamiz
                if not OlinganMaxsulot.objects.filter(
                    buyurtma=instance, maxsulot=buyurtma_maxsulot.maxsulot
                ).exists():
                    OlinganMaxsulot.objects.update_or_create(
                        buyurtma=instance,
                        maxsulot=buyurtma_maxsulot.maxsulot,
                        qiymat=buyurtma_maxsulot.qiymat,
                    )

            # OlinganMaxsulot qiymatlarini hisoblash
            for buyurtma_maxsulot in buyurtma_maxsulotlar:

                # Ombordagi jami mahsulot qiymatini hisoblash
                jami_qiymat = Ombor.objects.filter(maxsulot=buyurtma_maxsulot.maxsulot).aggregate(
                    total_qiymat=Sum('qiymat')
                )['total_qiymat'] or Decimal('0.00')

                # Olingan qiymatlarni hisoblash
                olingan_qiymat = OlinganMaxsulot.objects.filter(
                    maxsulot=buyurtma_maxsulot.maxsulot
                ).aggregate(total_qiymat=Sum('qiymat'))['total_qiymat'] or Decimal('0.00')

          
                # JamiMahsulotni yangilash
                jami_mahsulot, _ = JamiMahsulot.objects.get_or_create(maxsulot=buyurtma_maxsulot.maxsulot)
                jami_mahsulot.qiymat = jami_qiymat - olingan_qiymat
                jami_mahsulot.save()



        if instance.rad_etish:
            instance.active = False

            request = get_current_request()

            if not RadEtilganMaxsulot.objects.filter(buyurtma=instance).exists():
                RadEtilganMaxsulot.objects.create(buyurtma=instance, rad_etgan_user=request.user)


    # Bog'liq mahsulotlarni avtomatik yangilash (faqat validatsiya uchun)
    buyurtma_mahsulotlari = BuyurtmaMaxsulot.objects.filter(buyurtma=instance)
    for mahsulot in buyurtma_mahsulotlari:
        if mahsulot.qiymat <= 0:
            mahsulot.delete()


