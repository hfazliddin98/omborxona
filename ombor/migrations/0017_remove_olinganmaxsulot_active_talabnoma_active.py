# Generated by Django 4.2.16 on 2025-01-20 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ombor', '0016_olinganmaxsulot_maxsulot_olinganmaxsulot_qiymat_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='olinganmaxsulot',
            name='active',
        ),
        migrations.AddField(
            model_name='talabnoma',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
