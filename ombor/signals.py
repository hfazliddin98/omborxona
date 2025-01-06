from django.db.models.signals import post_save, post_delete
from django.db.models import Sum
from django.dispatch import receiver
from decimal import Decimal
from .models import Ombor, JamiMahsulot, OlinganMaxsulot

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
