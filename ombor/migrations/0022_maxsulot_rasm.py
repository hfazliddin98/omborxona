# Generated by Django 4.2.16 on 2024-12-07 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ombor', '0021_remove_buyurtma_izoh'),
    ]

    operations = [
        migrations.AddField(
            model_name='maxsulot',
            name='rasm',
            field=models.ImageField(null=True, upload_to='maxsulot'),
        ),
    ]
