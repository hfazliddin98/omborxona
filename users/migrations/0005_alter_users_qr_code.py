# Generated by Django 4.2.16 on 2024-11-27 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_users_qr_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='qr_code',
            field=models.CharField(max_length=300),
        ),
    ]