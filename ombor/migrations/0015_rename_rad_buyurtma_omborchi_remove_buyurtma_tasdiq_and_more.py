# Generated by Django 4.2.16 on 2024-12-02 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ombor', '0014_buyurtma_bugalter_izoh_buyurtma_it_park_izoh_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buyurtma',
            old_name='rad',
            new_name='omborchi',
        ),
        migrations.RemoveField(
            model_name='buyurtma',
            name='tasdiq',
        ),
        migrations.AddField(
            model_name='buyurtma',
            name='omborchi_izoh',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
