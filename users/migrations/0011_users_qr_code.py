# Generated by Django 4.2.16 on 2024-11-28 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_userqrcode_qr_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='qr_code',
            field=models.ImageField(null=True, upload_to='qr_code'),
        ),
    ]
