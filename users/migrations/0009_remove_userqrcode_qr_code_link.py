# Generated by Django 4.2.16 on 2024-11-28 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_userqrcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userqrcode',
            name='qr_code_link',
        ),
    ]
