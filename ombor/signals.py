from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ombor, JamiMahsulot
from django.db.models import F

@receiver(post_save, sender=Ombor)
def update_jami_mahsulot(sender, instance, created, **kwargs):
    if created:  # Faqat yangi mahsulot qo'shilganda
        jami_mahsulot, created = JamiMahsulot.objects.get_or_create(
            maxsulot=instance.maxsulot,
            defaults={'qiymat': 0, 'birlik': instance.birlik}
        )
        # `qiymat` maydoni `CharField` bo'lgani uchun oldin uni raqamga aylantiramiz
        jami_mahsulot.qiymat = str(int(jami_mahsulot.qiymat) + int(instance.qiymat))
        jami_mahsulot.save()
