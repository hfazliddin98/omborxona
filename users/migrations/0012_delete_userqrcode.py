# Generated by Django 4.2.16 on 2024-11-28 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_users_qr_code'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserQrCode',
        ),
    ]
