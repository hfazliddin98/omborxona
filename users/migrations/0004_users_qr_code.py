# Generated by Django 4.2.16 on 2024-11-27 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_admin_users_bugalter_users_it_park_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='qr_code',
            field=models.FileField(default=1, upload_to='user_qrcode'),
            preserve_default=False,
        ),
    ]
